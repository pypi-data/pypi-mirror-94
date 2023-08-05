import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sphinx-clutter-bazbazoo",
    version="0.0.1",
    author="Itay Donanhirsh",
    author_email="itay.donanhirsh@checkr.com",
    description="Sphinx Clutter plugin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cluttercode/sphinx-clutter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
