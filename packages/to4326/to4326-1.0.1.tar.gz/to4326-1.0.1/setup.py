import os
from setuptools import setup, find_packages


def load_readme():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join(".", "requirements.txt")
    with open(reqs_path, "r") as f:
        requirements = [line.rstrip() for line in f]
    return requirements


version = None
with open("to4326/__init__.py", "r") as fp:
    for line in fp:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip("\"'")
            break

setup(
    name="to4326",
    version=str(version),
    long_description_content_type="text/markdown",
    long_description=load_readme(),
    packages=find_packages(),
    author="yonda",
    author_email="yonda.fountain@gmail.com",
    url="https://github.com/yonda-yonda/to4326",
    install_requires=read_requirements(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    python_requires=">=3.7",
)