#!/usr/bin/env python

# https://packaging.python.org/tutorials/packaging-projects
# docker run -it  -v $PWD:/app  -w /app python:3.8  bash
# python3 -m pip install --user --upgrade twine
# python3 setup.py sdist clean
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --skip-existing --verbose dist/*

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mdbridge", # Replace with your own username
    version="0.4.2",
    author="xrgopher",
    author_email='xrgopher@outlook.com',
    url='https://gitlab.com/xrgopher/mdbridge',
    description="markdown extension for bridge PBN & xinrui & bbo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': [
            'mdbridge2html=mdbridge.mdbridge2html:main',
            'mdbridge2latex=mdbridge.mdbridge2latex:main',
            'lin2pbn=mdbridge.lin2pbn:main'
        ],
    },
    install_requires=[
        'xin2pbn','pbn2html'
    ],
    python_requires='>=3.6',
)
