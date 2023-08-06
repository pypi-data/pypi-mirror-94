"""
Objects/stringobject.c  Jan 2012 python source code


#### **`string_hash.c`**
```C
static long string_hash(PyStringObject *a)
{
    register Py_ssize_t len;
    register unsigned char *p;
    register long x;

    if (a->ob_shash != -1)
        return a->ob_shash;
    len = Py_SIZE(a);
    p = (unsigned char *) a->ob_sval;
    x = *p << 7;
    while (--len >= 0)
        x = (1000003*x) ^ *p++;
    x ^= Py_SIZE(a);
    if (x == -1)
        x = -2;
    a->ob_shash = x;
    return x;
}
```

```python
MAX_INT = 2**64
def string_hash(s):
    if isinstance(s, int):
        return -2 if s == -1 else s
    x = s[c] << 7
    for c in s.encode():
        x *= 1_000_003
        x = x ** c
    return x % MAX_INT - MAX_INT // 2
```
"""
