"""Package configuration for phytoolkit."""
from codecs import open

from setuptools import setup, find_packages

with open("README.md", "r", "utf-8") as readme:
    README = readme.read()

setup(
    name="phytoolkit",
    version="0.2.1-alpha",
    description="An installer toolkit for installing a bunch of common simulation tools",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Lallu Anthoor",
    author_email="lalluanthoor@gmail.com",
    url="https://github.com/lalluanthoor/phytools",
    packages=find_packages(),
    package_data={"": ["LICENSE", "README.md"]},
    include_package_data=True,
    python_requires=">=3.5",
    platforms=["Linux"],
    install_requires=[
        "click>=7.1.2",
        "colorama>=0.4.4",
        "requests>=2.25.1",
    ],
    entry_points={
        "console_scripts": [
            "phytoolkit=phytoolkit.phytoolkit:cli"
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering",
    ],
)
