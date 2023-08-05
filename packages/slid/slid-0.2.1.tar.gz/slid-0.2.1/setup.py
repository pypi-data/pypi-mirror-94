import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slid",
    version="0.2.1",
    author="Ram Taralekar",
    author_email="ramtaralekar@outlook.com",
    description="A package for making alert windows that slide close.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.com/project/slid",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)