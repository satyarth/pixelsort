import asyncio
import json
import pixelsort
from PIL import Image, ImageSequence, ImageFilter, ImageOps
from pixelsort import pixelsort as ps_func

async def process_image(input_path, mask_path, params_json, progress_callback=None):
    params = json.loads(params_json)
    img = Image.open(input_path)
    
    # --- Mask Loading ---
    mask_img = None
    if mask_path:
        mask_img = Image.open(mask_path).convert('L')
        if params['invert_mask']:
            mask_img = ImageOps.invert(mask_img)

    # --- Frame Detection Logic ---
    input_is_animated = getattr(img, "is_animated", False) and img.n_frames > 1
    user_wants_animation = (
        params['angle_start'] != params['angle_end'] or
        params['thresh_lower_start'] != params['thresh_lower_end'] or
        params['thresh_upper_start'] != params['thresh_upper_end'] or
        params['rand_start'] != params['rand_end'] or
        params['char_start'] != params['char_end'] or
        params['blur_start'] != params['blur_end']
    )
    
    target_frames = int(params.get('frame_count', 15))
    if not input_is_animated and not user_wants_animation:
        target_frames = 1

    original_frames = [f.copy() for f in ImageSequence.Iterator(img)]
    if len(original_frames) == 1 and target_frames > 1:
        original_frames = [original_frames[0]] * target_frames
    
    total_frames = len(original_frames)
    processed_frames = []

    # --- FPS & Duration Logic ---
    fps = int(params.get('fps', 10))
    duration_ms = int(1000 / fps)
    if params.get('use_source_fps', False) and 'duration' in img.info:
         if img.info['duration'] > 20: duration_ms = img.info['duration']

    # --- Processing Loop ---
    for i, frame in enumerate(original_frames):
        if progress_callback:
            progress_callback(i + 1, total_frames)
        await asyncio.sleep(0) # Yield for UI update

        t = i / (total_frames - 1) if total_frames > 1 else 0
        
        # Interpolate all parameters
        cur_ang = params['angle_start'] + (params['angle_end'] - params['angle_start']) * t
        cur_tl = params['thresh_lower_start'] + (params['thresh_lower_end'] - params['thresh_lower_start']) * t
        cur_tu = params['thresh_upper_start'] + (params['thresh_upper_end'] - params['thresh_upper_start']) * t
        cur_rnd = params['rand_start'] + (params['rand_end'] - params['rand_start']) * t
        cur_cl = params['char_start'] + (params['char_end'] - params['char_start']) * t
        cur_blr = params['blur_start'] + (params['blur_end'] - params['blur_start']) * t

        work_frame = frame.convert("RGB")
        if cur_blr > 0:
            work_frame = work_frame.filter(ImageFilter.GaussianBlur(cur_blr))

        cur_mask = None
        if mask_img:
            cur_mask = mask_img.resize(work_frame.size)

        try:
            sorted_frame = ps_func(
                work_frame,
                mask_image=cur_mask,
                interval_function=params['interval_func'],
                sorting_function=params['sort_func'],
                lower_threshold=float(cur_tl),
                upper_threshold=float(cur_tu),
                randomness=float(cur_rnd),
                char_length=float(cur_cl),
                angle=float(cur_ang)
            )
            processed_frames.append(sorted_frame)
        except Exception as e:
            processed_frames.append(work_frame)

    # --- Save & Export ---
    output_path = "/output.gif"
    processed_frames[0].save(
        output_path, save_all=True, append_images=processed_frames[1:],
        duration=duration_ms, loop=0
    )
    with open(output_path, "rb") as f:
        return f.read()