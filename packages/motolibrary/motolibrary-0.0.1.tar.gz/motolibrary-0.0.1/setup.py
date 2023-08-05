# setup.py
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="motolibrary", # Replace with your own username
    version="0.0.1",
    author=" Dylan Doyle ",
    author_email="ddoyle@motoinsight.ca",
    description="Library of useful functions for custom solutions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/motoinsight-data-ops/motolibrary",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
