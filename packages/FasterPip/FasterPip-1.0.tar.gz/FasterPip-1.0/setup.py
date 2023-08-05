from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="FasterPip", # Replace with your own username
    version="1.0",
    author="mstouk57g",
    author_email="mstouk57g@yeah.net",
    description="Faster pip for Python users can be used to install Python modules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mstouk57g/FasterPip",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.0',
)
