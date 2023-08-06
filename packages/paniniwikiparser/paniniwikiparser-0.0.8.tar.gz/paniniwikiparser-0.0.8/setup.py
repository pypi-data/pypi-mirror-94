import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paniniwikiparser", # Replace with your own username
    version="0.0.8",
    author="Anil Vemula",
    author_email="v-anvemu@microsoft.com",
    description="Parses wiki xml",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://o365exchange.visualstudio.com/O365%20Sandbox/_git/IPMLExp?path=%2Fsrc%2FPanini2%2FSyntheticDataGenerator&version=GBmaster",
    packages=setuptools.find_packages(),
    install_requires=['six','nltk','python-dateutil','nameparser','PyMySQL','mwparserfromhell '],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)