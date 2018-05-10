# Coursera Dump

This script saves in *.xlsx file information about 20 random
courses of [Coursera](https://www.coursera.org). 

# How To Install

Python v3.5 should be already installed. 
Afterwards use pip (or pip3 if there is a conflict with old Python 2 setup)
to install dependecies:

```bash
pip install -r requirements.txt # alternatively try pip3
```
Remember that it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) 
for better isolation.

# Quick Start

The script has one optional argument - full path of output file.
By default the script outputs result in `courses_info.xlsx` located
in script`s directory.

Output file contains these course features: name,
language, start date, weeks of study, course rating and URL.

To run script on Linux:
```bash
$ python coursera.py -o courses.xlsx
```
Windows usage is the same.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
