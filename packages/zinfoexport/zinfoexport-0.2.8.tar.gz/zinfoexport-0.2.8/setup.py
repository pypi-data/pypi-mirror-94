import setuptools
import os 

with open("README.md", "r") as fh:
   long_description = fh.read() 

setuptools.setup( 
    name="zinfoexport",
    version = "0.2.8",
    author = "Tobias Cadée",
    author_email = "t.cadee@hhsk.nl",
    description="Package to extract data from z-info (historian)",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url="https://gitlab.com/tcadee/z-info-export-client",
    packages = setuptools.find_packages(),
    install_requires=[
        'pandas',
        'requests'
    ],
    python_requires = ">=3.6"
)