"""setup."""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyFina",
    version="0.0.5",
    author="Alexandre CUER",
    author_email="alexandre.cuer@wanadoo.fr",
    description="A numpy subclass to read emoncms PHPFINA feeds as numpy array",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Open-Building-Management/PyFina",
    project_urls={
        "Bug Tracker": "https://github.com/Open-Building-Management/PyFina/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'matplotlib'
    ],
    python_requires=">=3.6",
)
