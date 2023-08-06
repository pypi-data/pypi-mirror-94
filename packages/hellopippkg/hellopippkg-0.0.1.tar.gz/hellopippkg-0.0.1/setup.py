import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hellopippkg",
    version="0.0.1",
    #author="KS",
    #author_email="ks@bt.com",
    description="Simply display HELLO PIP!!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="www.ks.com",
    packages=setuptools.find_packages(),
    include_package_data=True
    # install_requires=["PyYAML", "pandas"],
    # classifiers=[
    #    "Programming Language :: Python :: 3.7",
    #    "License :: OSI Approved :: MIT License",
    #    "Operating System :: OS Independent",
    # ],
)
