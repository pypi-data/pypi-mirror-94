# pykvs

PyKVS is key-value store for Python. keys must be string and values must be picklable object.

## Installation

```python
git clone https://github.com/yutayamazaki/pykvs.git
python setup.py install
```

## Example

```python
import pykvs

kvs = pykvs.PyKVS('./kvs')
kvs['some-key'] = 'some-value'
```
