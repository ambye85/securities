# Securities

Securities is a tool for performing simple analytics on a data set.

## Pre-requisites

Running the securities tool locally requires the following pre-requisites to be installed:

- [Poetry](https://python-poetry.org): `pip install poetry` 

## Running

The securities tool can be run using your system installed Python 3:

```shell script
./securities.py
```

You can also execute securities from within a Poetry environment:

```shell script
poetry install
poetry run cli
```

## Testing

To run the suite of tests you will require Poetry to be installed, then execute:

```shell script
poetry install
poetry run pytest
```
