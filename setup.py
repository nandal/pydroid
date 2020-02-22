import setuptools
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


with open("README.md", "r", encoding="utf-8") as fd:
    long_description = fd.read()

setuptools.setup(
    name='pydroid',  
    version='0.1',
    scripts=['sample_test_script.py'],
    author="Sandeep Nandal",
    author_email="sandeep@nandal.in",
    description="An Android Device Automation Framework package to control ADB using shell",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nandal/pydroid",
    packages=["pydroid"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='pydroid android automation adb tools',
    install_requires=['pathlib']
)
