#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='predicto',
    version='1.0.0',
    description='A sequence generator to extract frames uniformly from a video and feed it to a time-distributed layer, without labels.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Atharva Peshkar and Atharva Khedkar',
    author_email='peshkaratharva@gmail.com',
    url='https://github.com/Atharva-Peshkar/predicto',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    python_requires=">=3.5",
    install_requires=[
        'keras>=2',
        'numpy',
        'opencv-python',
        'matplotlib'
    ]
)
