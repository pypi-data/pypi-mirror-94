from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="padio",
    version="1.0.1",
    description="Zero pad numeric filenames",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.iamthefij.com/iamthefij/padio.git",
    download_url=("https://git.iamthefij.com/iamthefij/padio/releases"),
    author="iamthefij",
    author_email="ian@iamthefij.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="",
    py_modules=["padio"],
    entry_points={
        "console_scripts": [
            "padio=padio:main",
        ],
    },
)
