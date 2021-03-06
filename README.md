# Symposium
A web based classroom app written in [Python](https://www.python.org/) using
[Django Framework](https://www.djangoproject.com/)
adapted for higher institutions.

## Features
1. Personalized student dashboards.
2. Timetable and lecture updates.
3. Support for mathematical and chemical equations using [katex](https://katex.org/) and [mhchem](https://mhchem.github.io/MathJax-mhchem/)

## Setting it up.
Note: it is required that you have some level
of familiarity with Python, and that you have python3 and pipenv
installed on your local environment.

If you don't have pipenv installed, you can get it
installed like so.
```bash
$ python3 -m pip install pipenv
```

To go ahead and set up this project in your local
environment first you have to clone this repository
```bash
$ git clone https://github.com/gray-adeyi/symposium.git
$ cd symposium
$ pipenv install
```
After successful installation of project dependencies,
```bash
$ pipenv shell
$ ./manage.py runserver
```
Visit the server on http://localhost:8000

## Contributors.
* Gbenga Adeyi
