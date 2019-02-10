import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="munichways_data",
    version="0.0.1",
    author="Jan Langfellner",
    author_email="contact@jan-langfellner.de",
    description="A package to process data for the RadlVorrangNetz",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MunichWays/daten.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)