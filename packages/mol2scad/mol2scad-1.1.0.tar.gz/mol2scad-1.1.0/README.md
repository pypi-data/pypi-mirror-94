# mol2scad

![gpl3.0](https://img.shields.io/github/license/Paradoxdruid/pychemistry.svg "GPL 3.0 Licensed")  [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Paradoxdruid/pychemistry.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Paradoxdruid/pychemistry/context:python)  [![CodeFactor](https://www.codefactor.io/repository/github/paradoxdruid/pychemistry/badge)](https://www.codefactor.io/repository/github/paradoxdruid/pychemistry) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) ![PyPI](https://img.shields.io/pypi/v/mol2scad)

**mol2scad** is a script to turn molecular coordinates into SCAD files.  Takes molfile / sdf coordinates as input, outputs a scad file for OpenSCAD.

## Usage

```
python mol2scad.py -i <input molfile> -o <output scadfile>
```

or if installed via `pip install mol2scad`:
```
mol2scad -i <input molfile> -o <output scadfile>
```

A useful tool to [obtain mol files](https://cccbdb.nist.gov/mdlmol1.asp) is available via NIST.

## Authors

Implementation builds on on makebucky.scad at http://www.thingiverse.com/thing:12675 by [Paul Moews](https://www.thingiverse.com/pmoews/designs).

This script is developed as academic software by [Dr. Andrew J. Bonham](https://github.com/Paradoxdruid) at the [Metropolitan State University of Denver](https://www.msudenver.edu).
