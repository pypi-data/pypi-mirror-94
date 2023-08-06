pytest-custom-concurrency: pytest plugin
==============

Rewrite pytest_runtestloop function, Using thread to realize concurrent running.

install
=====

`pip install `

Usage
=====

command line:`pytest --concurrent={on:off} --sub_group=str`

- concurrent: Used to open plugin, default "off"
- sub_group: Used to customize grouping parameters, default "group"

demo
=====

```python
import pytest


@pytest.mark.parametrize("name", ["group_1", "group_2", "group_3"])
def test_04(name):
    a = "hello"
    b = "world"
    assert a == b


@pytest.fixture(name="name")
def add_param():
    return "group_1"

def test_01(name):
    pass
```

cmd line: `pytest --concurrent=on sub_group=name`