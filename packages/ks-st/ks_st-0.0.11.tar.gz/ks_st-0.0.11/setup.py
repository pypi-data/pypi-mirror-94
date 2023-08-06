import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ks_st", # Replace with your own username
    version="0.0.11", author="Armandpl",
    author_email="adpl33@gmail.com",
    description="Style transfer toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Armandpl/ks_st",
    install_requires=[
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
