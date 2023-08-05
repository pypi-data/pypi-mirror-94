# garfetch

Python 3 library to fetch comic images from gocomics.com.

## Installation

### PyPI

This package is available on PyPI as `garfetch`.

### Building

This project uses [poetry](https://python-poetry.org/), and the recommended way of building it is running `poetry build` on the root of this repository.

## Usage

### Get comic URL

`garfetch.fetch_url(comic, datestr)` can be used to fetch comic URL for a given comic on a given day. Comic slug can be extracted from a gocomics URL. Date format is `YYYY-MM-DD` or `YYYY/MM/DD`.

```python
import garfetch

print(garfetch.fetch_url("garfield", "1990-05-30"))
# 'https://assets.amuniversal.com/7e81c7c05d1a012ee3bd00163e41dd5b'
```

A non-existant comic or a server error will currently throw an AssertionError. This behavior may be changed in the future.

### Get comic calendar

`garfetch.fetch_calendar(comic, datestr)` can be used to fetch a list of comics available on a given month. Comic slug can be extracted from a gocomics URL. Date input format is `YYYY-MM` or `YYYY/MM`. Date output format is a list of `YYYY/MM/DD`s.

```python
import garfetch

print(repr(garfetch.fetch_calendar("garfield-classics", "2020-07")))
# ['2020/07/01', '2020/07/02', '2020/07/03', '2020/07/04', '2020/07/05', '2020/07/06', '2020/07/07', '2020/07/08', '2020/07/09', '2020/07/10', '2020/07/11', '2020/07/12', '2020/07/13', '2020/07/14', '2020/07/15', '2020/07/16', '2020/07/17', '2020/07/18', '2020/07/19', '2020/07/20', '2020/07/21', '2020/07/22', '2020/07/23', '2020/07/24', '2020/07/25', '2020/07/26', '2020/07/27', '2020/07/28', '2020/07/29', '2020/07/30', '2020/07/31']

print(repr(garfetch.fetch_calendar("garfield-classics", "2019-01")))
# ['2019/01/07', '2019/01/08', '2019/01/09', '2019/01/10', '2019/01/11', '2019/01/12', '2019/01/13', '2019/01/14', '2019/01/15', '2019/01/16', '2019/01/17', '2019/01/18', '2019/01/19', '2019/01/20', '2019/01/21', '2019/01/22', '2019/01/23', '2019/01/24', '2019/01/25', '2019/01/26', '2019/01/27', '2019/01/28', '2019/01/29', '2019/01/30', '2019/01/31']
```

A non-existant comic or a server error will currently throw an AssertionError. This behavior may be changed in the future.
