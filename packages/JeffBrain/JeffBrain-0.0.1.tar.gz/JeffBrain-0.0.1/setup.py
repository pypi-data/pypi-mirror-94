from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Vocal Assisstant'

# Setting up
setup(
    name="JeffBrain",
    version=VERSION,
    author="Gauthegoat (Gauthier Bassereau)",
    author_email="<gauthier.bassereau@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['speech_recognition', 'pyttsx3','pywhatkit','datetime','wikipedia','time','urllib.request','googletrans','os','webbrowser','subprocess','time'],
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