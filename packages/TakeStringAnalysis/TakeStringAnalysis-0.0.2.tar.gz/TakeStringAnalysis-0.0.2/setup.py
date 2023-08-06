import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="TakeStringAnalysis",
    version="0.0.2",
    author="Renan Santos Mendes",
    author_email="renans@take.net",
	keywords='string',
    description="This package returns a similar string from a stream",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
	install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	include_package_data = True
)