# google-places-searcher

A simple script to searching on google places with Python

## Install

First, install the requirement :

```shell
pip install -r requiements.txt
```

## Run the script

Here is the available option (* is not require) :

- -t : *for testing usage with `-f` if you want to precise the test file. Otherwise `exemple.json` will be use.
- -f : *relative path to the test file
- -n : *precise the maximum number of result to get from Google
- -q : the query, for exemple `tutoring company London`

And now the command :

```shell
python ./script.py -n 200 -q "tutor company france"
```
