# date-range-cli
A cli tool that iterates through a range of dates

## How to install

```sh
pip install date-range-cli
```


## Usage
Get a range of dates:
```sh
daterange -s 2020-01-01 -e 2020-01-05
2020-01-01 2020-01-02 2020-01-03 2020-01-04 2020-01-05
```

Get a date range since a start date til now:
```sh
daterange -s 2021-02-08
2021-02-08 2021-02-09 2021-02-10 2021-02-11 2021-02-12
```

Custom format range of dates:
```sh
daterange -s 2020-01-01 -e 2020-01-05 -f %m_%d_%Y
01_01_2020 01_02_2020 01_03_2020 01_04_2020 01_05_2020
```
The format follows strftime defined by python: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

### Todos

 - Support hours instead of just days
 - Need to add granularity (hr vs day) to iterate on a single hour from day to day
