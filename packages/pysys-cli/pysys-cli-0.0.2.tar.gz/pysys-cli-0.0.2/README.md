[![PyPI](https://img.shields.io/pypi/v/pysys-cli.svg)](https://pypi.org/project/pysys-cli/) <img src="https://github.com/Yangzhenzhao/pysys-cli/workflows/CI/badge.svg" />


### Installation

`pip install --upgrade pysys-cli`        


### Cli

```
$ syscli --help
Usage: syscli [OPTIONS]

Options:
  -c, --cpu
  -m, --memroy
  -d, --disk
  --help        Show this message and exit.

$ syscli -c
2.30 GHz 2核 4线程

$ syscli -d
total: 250.69G
free: 69.53G
```
