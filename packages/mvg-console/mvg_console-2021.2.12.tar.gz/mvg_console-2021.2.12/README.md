# A console program to request the departure time from the MVG

This python script is a Command Line wrapper to get the departures from any station/stop in the MVG(Münchner Verkehrsgesellschaft) network. Based on the [mvg_api](https://github.com/leftshift/python_mvg_api) project.

## Getting started
- install the package: `pip install mvg-console`

## Usage
```
usage:
mvg [--help][version][dest][search]

Commands:
dest: Print departure info for destination
-----
usage: mvg dest [OPTIONS] STATION

Arguments:
  STATION  [required] Destination Station to display ifno for.

Options:
  --limit INTEGER  [default: 10]
  --mode TEXT
  --help           Show this message and exit.

search: find nearest stops to the address
-------
Usage: mvg search [OPTIONS] QUERY

Arguments:
  QUERY  [required] address to find nearest stops for.

Options:
  --help  Show this message and exit.

version: display package version
--------
Usage: mvg version
```

## Demo
![screenshot](demo.png)

## Changelog
#### 12.02.2021
- Move to [Typer](http://typer.tiangolo.com) instead of argparse.
- Handle some errors.
- Move to [prettytable](https://pypi.org/project/prettytable/) instead of Texttable.
- Disable HistoryManager.
#### 12.11.2018
* We're on PyPi! Now you can easily install the script using pip!
* You can now search for the nearest station/stop from an address! Use the --search/-s [adress]
* You can choose the Transportation mode to be displayed using the --mode/-m arguement. Available modes: bus, ubahn, sbahn, tram.
* A lot of Bug Fixes.
