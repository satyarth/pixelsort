import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
    name="pixelsort",
    version="1.0.1",
    author="Bernard Zhao",
    author_email="bernardzhao@berkeley.edu",
    description="An image pixelsorter for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/satyarth/pixelsort",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
