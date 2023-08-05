import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="underscoreclass",
    version="0.1.0",
    description="\"(_^o^_)\" can now be valid Python syntax.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Seth Peace",
    author_email="sethevanpeace@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["underscoreclass"],
    include_package_data=True,
)
