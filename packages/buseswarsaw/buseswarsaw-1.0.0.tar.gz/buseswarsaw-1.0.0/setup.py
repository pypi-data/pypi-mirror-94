from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="buseswarsaw",
    version="1.0.0",
    description="Python package containing tools for analysing data on buses in Warsaw",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/BDomzal/buses-in-Warsaw-bd",
    author="Barbara Domżał",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ],
    packages=["buses_warsaw"],
    include_package_data=True,
    install_requires=["numpy", "pandas", "geopy", "matplotlib"]
)
