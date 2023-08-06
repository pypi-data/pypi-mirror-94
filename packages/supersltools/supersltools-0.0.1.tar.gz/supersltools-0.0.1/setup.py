from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'tools for work'


# Setting up
setup(
    name="supersltools",
    version=VERSION,
    author="Snehashish Laskar",
    author_email="<snehashish.laskar@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['turtle', 'pyjokes', 'gTTS', 'gtts', 'SpeechRecognition', 'playsound', 'pyaudio', 'wikipedia', 'pywhatkit', 'pyttsx3'],
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