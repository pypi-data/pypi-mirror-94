# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='toppy',
    version='0.1.3',
    description='Graphical system resources monitor in python',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Roi Gabay',
    author_email='roigby@gmail.com',
    url='https://github.com/gabay/toppy',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    packages=find_packages(exclude=('test',)),
    install_requires=[
        'matplotlib>=3.3.4,<4',
        'psutil>=5.8.0,<6',
        'gpustat>=0.6.0,<1'
    ],
    tests_require=['pytest>=6.2.2,<7']
)
