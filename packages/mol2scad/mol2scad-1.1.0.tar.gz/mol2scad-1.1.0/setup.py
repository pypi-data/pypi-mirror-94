"""Setup module for mol2scad.
"""

# Always prefer setuptools over distutils
from setuptools import setup
from pathlib import Path

here = Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Setup via pip
setup(
    name="mol2scad",
    version="1.1.0",
    author="Andrew J. Bonham",
    author_email="abonham@msudenver.edu",
    description="A script to turn molecular coordinates files into SCAD files",
    license="GPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Paradoxdruid/pychemistry/tree/master/scripts/mol2scad",
    py_modules=["mol2scad"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    keywords="chemistry, buffer, biochemistry",
    python_requires=">=3.6",
    entry_points={"console_scripts": ["mol2scad = mol2scad:main"],},
)
