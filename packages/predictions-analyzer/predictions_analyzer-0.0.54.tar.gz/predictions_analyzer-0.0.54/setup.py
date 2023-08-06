import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="predictions_analyzer",
    version="0.0.54",
    author="Thomas Meli",
    author_email="tpmeli.data@gmail.com",
    description="A powerful tool for analyzing and ensembling predictions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThomasMeli/predictions_analyzer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

import predictions_analyzer
