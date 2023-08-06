from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'Simple package for making the program speak'
LONG_DESCRIPTION = 'Rather than using long instance making and all that, you can just type speak to make the program speak'

# Setting up
setup(
    name="spk",
    version=VERSION,
    author="Aditya Singh",
    author_email="<mail@yusiferzendric.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyttsx3'],
    keywords=['python', 'speaking', 'simple speaking', 'speak', 'bot speaking'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)