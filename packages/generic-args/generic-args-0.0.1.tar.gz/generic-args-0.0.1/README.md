# generic-args

[![Build Status](https://github.com/python-platonic/generic-args/workflows/test/badge.svg?branch=master&event=push)](https://github.com/python-platonic/generic-args/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/python-platonic/generic-args/branch/master/graph/badge.svg)](https://codecov.io/gh/python-platonic/generic-args)
[![Python Version](https://img.shields.io/pypi/pyversions/generic-args.svg)](https://pypi.org/project/generic-args/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

Given an instantiated generic class, retrieve the type arguments of itself or its parents.

The packages solves the problem described at [this StackOverflow question](https://stackoverflow.com/q/48572831/1245471).

## Installation

```bash
pip install generic-args
```


## Example

Showcase how your project can be used:

```python
from typing import List
from generic_args import generic_type_args

generic_type_args(List[int])
# (<type 'int'>, )
```

## License

[MIT](https://github.com/python-platonic/generic-args/blob/master/LICENSE)


## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [54efe958f72ac06e912a1423aa14be8b149f988f](https://github.com/wemake-services/wemake-python-package/tree/54efe958f72ac06e912a1423aa14be8b149f988f). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/54efe958f72ac06e912a1423aa14be8b149f988f...master) since then.
