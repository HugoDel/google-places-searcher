# google-places-searcher

A simple script to searching on google places with Python 3

## Install

First, install the requirement :

```shell
pip install -r requiements.txt
```

## Run the script

Here is the available option :

| Option | Description | Mandatory |
| ------ | ----------- | --------- |
| -t     | for testing usage with `-f` if you want to precise the test file. Otherwise `exemple.json` will be use | No |
| -f     | relative path to the test file | |
| -n     | precise the maximum number of result to get from Google, should be a multiple of 20 | No |
| -q     | the query, for exemple `tutoring company London | Yes |
| -o     | the output file to write in case `-s` option usage. If not precise, data will be written to `results.json`  | No |
| -s     | save the result | No |
| -k     | keep the actuel content of the result file | No |

And now the command :

```shell
python ./script.py -n 200 -q "tutor company france" -ks -o `my_result.json`
```
