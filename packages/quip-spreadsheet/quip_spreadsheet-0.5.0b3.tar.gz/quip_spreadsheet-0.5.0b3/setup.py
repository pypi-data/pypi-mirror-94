import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="quip_spreadsheet",
    version="0.5.0b3",
    description="An opinionated client to search, retrieve, and parse Quip spreadsheets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Andrea Amorosi",
    url="https://github.com/dreamorosi/quip-spreadsheet",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests~=2.25",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
