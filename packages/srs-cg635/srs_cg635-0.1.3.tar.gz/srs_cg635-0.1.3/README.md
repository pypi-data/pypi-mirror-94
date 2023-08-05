![Build Status](https://github.com/l-johnston/srs_cg635/workflows/publish/badge.svg)
![PyPI](https://img.shields.io/pypi/v/srs_cg635)
# `srs_cg635`
Python interface to the Stanford Research Systems CG635 Clock Generator

## Installation
```cmd
> pip install srs_cg635
```  

## Usage

```python
>>> from srs_cg635 import CommChannel
>>> with CommChannel(address=23) as cg:
...     cg.frequency = 10e6 # Hz
...     cg.cmos_levels = "3.3 V"
>>> 
```

Supported features:
- frequency
- phase
- output levels
- output run state
- status
