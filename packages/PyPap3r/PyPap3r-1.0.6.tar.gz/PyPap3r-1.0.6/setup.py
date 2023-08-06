import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyPap3r", 
    version="1.0.6",
    author="TheBaconPug",
    description="A python package that can change your mac's wallpaper to a file or a url. It can also download images.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheBaconPug/PyPap3r",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ],
    python_requires='>=3.8',
)