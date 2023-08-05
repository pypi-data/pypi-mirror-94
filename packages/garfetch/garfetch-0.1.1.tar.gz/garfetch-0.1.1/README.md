# garfetch

Python 3 library to fetch comic images from gocomics.com.

## Installation

### PyPI

This package is available on PyPI as `garfetch`.

### Building

This project uses [poetry](https://python-poetry.org/), and the recommended way of building it is running `poetry build` on the root of this repository.

## Usage

### Get comic URL

```python
import garfetch

print(garfetch.fetch_url("garfield", "1990-05-30"))
# If comic exists: 'https://assets.amuniversal.com/7e81c7c05d1a012ee3bd00163e41dd5b'
# If comic does not exist: None
```
