# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 13:30:12 2021

@author: sashank
"""

from setuptools import setup, find_packages
import codecs
import os

#here = os.path.abspath(os.path.dirname(__file__))

#with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'HelloWorldAbc'
LONG_DESCRIPTION = 'A package that allows to build Hello World Abcc.'

# Setting up
setup(
    name="hellopackageabc",
    version=VERSION,
    author="Sashank_Narayan",
    author_email="<sashank99narayan@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'pyautogui'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)