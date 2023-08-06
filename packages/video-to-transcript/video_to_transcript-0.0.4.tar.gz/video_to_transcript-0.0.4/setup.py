from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.4'
DESCRIPTION = 'Video speech Extracter'
LONG_DESCRIPTION = 'Extract the Speech from the video file to readable text format'

# Setting up
setup(
    name="video_to_transcript",
    version=VERSION,
    author="Asher Mathews Shaji",
    author_email="msasher123@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['moviepy', 'SpeechRecognition'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets','transcript'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)