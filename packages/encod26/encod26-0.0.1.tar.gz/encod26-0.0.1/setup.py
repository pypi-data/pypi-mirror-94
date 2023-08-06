from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'String encoder'


# Setting up
setup(
    name="encod26",
    version=VERSION,
    author="Aryan Katiyar",
    author_email="aryankatiyar1420@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",

    packages=find_packages(),
    install_requires=['hashlib'],
    keywords=['python', 'encoder', 'string', 'password'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)