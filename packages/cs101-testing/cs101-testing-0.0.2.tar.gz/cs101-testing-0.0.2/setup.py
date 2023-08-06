import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "cs101-testing",
    version = "0.0.2",
    url = "https://github.com/karthiksharma/cs101-testing",
    author = "Kartikeya Sharma",
    author_email = "ksharma@illinois.edu",
    classifiers =
        ["Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    description = "Testing module for cs101 labs",
    packages = setuptools.find_packages(),
    long_description = long_description,
    long_description_content_type = "text/markdown",
    python_requires='>=3.0',
)