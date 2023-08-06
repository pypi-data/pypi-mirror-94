from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Easily write code'


# Setting up
setup(
    name="EasyCode",
    version=VERSION,
    author="Python.Stuff",
    author_email="<srinathngudi11@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyautogui', 'pyttsx3', 'speechrecognition'],
    keywords=['python', 'easy', 'code'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
