# jsiter
JavaScript flavor iterable for python.

### install
```
pip install jsiter
# or
pip3 install jsiter
# depends on your OS
```

#### Before
```python
from functools import reduce

a = [1,3,5,7,9,100]

reduce(lambda a,b:a+b,map(lambda x:chr(x),sorted(filter(lambda x:x<=90,map(lambda x:x+65,a)),key=lambda x:-x)))
# 'JHFDB'
```

#### After

```python
from jsiter import jsiter

a = jsiter([1,3,5,7,9,100])

a.map(lambda x:x+65).filter(lambda x:x<=90).sorted(key=lambda x:-x).map(lambda x:chr(x)).reduce(lambda a,b:a+b)
# 'JHFDB'
