from setuptools import setup, find_packages
import os

def read(rel_path):
    with open(rel_path, "r", encoding="utf-8") as fh:
        return fh.read()
def version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            # __version__ = "2.0"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

setup(
    name="FasterPip",
    version=version("FasterPip/__init__.py"),
    author="mstouk57g",
    author_email="mstouk57g@yeah.net",
    description="Faster pip for Python users can be used to install Python modules",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://mstouk57g.github.io/FasterPip/",
    project_urls={
        "Documentation": "https://github.com/mstouk57g/FasterPip/blob/main/README.md",
        "Source": "https://github.com/mstouk57g/FasterPip",
        "Changelog": "https://github.com/mstouk57g/FasterPip/releases",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
    ],
    python_requires='>=3.9.0',
)
