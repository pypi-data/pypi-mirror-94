problem - inconsistent - title - hashes.md

# The humble `hash`

You might think that Python's humble, behind-the-scenes, built-in `hash` function couldn't cause you much trouble.
I sure did.

# Problem

I `hash` the 15M unique Wikipedia article titles to try to cut down on the memory required to store all those strings in RAM.
Unfortunatley, each time I rehashed them, compressed them with `gzip`, and saved them to disk and uploaded them to Digital Ocean, they seemeed to change slightly.
The file size would change by a few bytes out of Millions of bytes.
And I couldn't find the hashes for potential new titles in those lists of hashes after reloading them from Digial Ocean.

I eventually traced the problem to the hash function itself.
Bottom line: don't ever make any assumptions about low level functions like `hash`.  RTFM!!!

# What are hashes for?

Hashes are usually used when you want to create an abbreviated, usually numerical digest of a long string.
When you call `hash('some long string')` in python, you get back a long integer that uniquely represents the exact string you put into it.
That way you can check for membership in a `set` of `dict` just by comparing integers instead of comparing all the integer representations of all the characters in all the strings in your set.

# What do you look for in a hash function

Because hashes reduce, or compress a lot of information into a small number of digits there will enevitably be more than one hash representation of many strings.
It's called a collision whenever one object can be hashed to more than one value.
The best hash functions avoid this as much as possible because it requires you to then check the individual elements for each colliding object to finally resolve the collision.

# What gives?

It seems that Python _improved_ the hash function in the transitoin from Python 2 to Python 3.
Some of the speed improvements you see in Python 3 are the result of little things like this.
The `hash` function is used within the `dict` and `set` and many other data structures.
Collisions can slow a lot of operations like inserts and __get_item__ operations.

So the core developers concatenated a salt(a random string) string to the end of any string being hashed.
This works to more evenly distribute the hash values across all the available long int values between - 2 ^ 63 and +2 ^ 64.
And they randomly generate a new `PYTHONHASHSEED` value each time a python process is launched.

You have two options, if you want to have a hash value that is consistent across sessions and workers:

1. set the environment variable for the hash seed to an int between 0 & 4294967295: `export PYTHONHASHSEED = 123456`
2. use a hash function within hashlib that does not salt the hash: e.g. `hashlib.md5`


# Wrapper Tests


```python


def test_hash_speed():
    runtime = 0
    for i in range(10):
        t0 = time.time()
        for j in range(1000):
            md5('barackobama' + str(j), 16)
        t1 = time.time()
        runtime += (t1 - t0) / 1000 / 10
    assert runtime < 1e-4
    return runtime


test_hash_speed()
```


```python
from qary.etl.scrape_wikipedia import *
ws = WikiScraper()
md5(normalize_title(r'!!!f&%U--c)$kyO0U!!!')) in ws.title_hashes[:100]
# True
md5('fu') in ws.title_hashes[5000:8000]
# True
hashes = read_and_hash_titles(chunksize=1000, numchunks=8)
hashes.shape
# (8000,)
```

```python
from qary.etl.scrape_wikipedia import *
ws = WikiScraper()
ws.filtered_titles('Barack Obama,barack,fuj'.split(','))
['Barack Obama', 'barack']
```

Check collision probability by seeing how often a random string hashes to the same value as something in a wikipedia title.
Use the pd.Series dictionary of hashes to find some reverse hashes for wikipedia titles and show how that would apply to cryptographic hashes of passwords and how salt makes that harder.

```python
>>> import this
>>> this.s
"Gur Mra bs Clguba, ...
>>> hash(this.s)
```

```python
>>> 123 << 7
15744
>>> 255 << 7
32640
>>> 256 << 7
32768
>>> 256 * 2**7
32768
>>> x = object()
>>> x.__str__()
'<object object at 0x7f30f4863ba0>'
>>> hash(x)
8740514849722
>>> y.__str__()
>>> y = object()
>>> hash(y)
8740514849677
>>> hex(hash(y))
'0x7f30f48638d'
>>> class Imaginary:
...     real = None
...     imag = None
...
>>> num = Imaginary()
>>> num.real = 1
>>> num.imag = 2
>>> str(num)
'<__main__.Imaginary object at 0x7f30d0048310>'
>>> hash(num)
8740476569649
>>> num.imag = 3
>>> hash(num)
8740476569649
>>> class Imaginary:
...     real = None
...     imag = None
...     def __str__(self)
...
>>> class Imaginary:
...     real = None
...     imag = None
...     def __str__(self):
...         return f'Imaginary(real={self.real}, imag={self.imag}'
...
>>> num = Imaginary()
>>> hash(num)
8740476570745
>>> num.imag = 3
>>> hash(num)
8740476570745
>>> num.real = 1
>>> hash(num)
8740476570745
>>> str(num)
'Imaginary(real=1, imag=3'
>>> hash(1)
1
>>> hash(2)
2
>>> hash(-2)
-2
>>> hash(-1)
-2
```

```python
>>> x = object()
>>> hash(x)
8739771162946
>>> x.whatever = 5
>>> x.__doc__ = 'whatever'
>>> hash(str(x))
-2355294420857791440
>>> hash(x.__str__())
-2355294420857791440
>>> hash(x.__repr__())
-2355294420857791440
>>> hash(repr(x))
-2355294420857791440
>>> hash(x)
8739771162946
>>> str(x)
'<object object at 0x7f2e2f4a1420>'
>>> x
<object at 0x7f2e2f4a1420>
>>> repr(x)
'<object object at 0x7f2e2f4a1420>'
>>> x.id
>>> id(x)
139836338607136
>>> hash(x)
8739771162946
>>> hex(hash(x))
'0x7f2e2f4a142'
>>> hex(id(x))
'0x7f2e2f4a1420'
>>> x
<object at 0x7f2e2f4a1420>
>>> import this
>>> hash(this.s)
-4953155752906756154
>>> sum(ord(c) for c in this.s)
78459
>>> this.s.__str__()
"Gur Mra bs Clguba, ol Gvz Crgref\n\nOrnhgvshy vf orggre guna htyl.\nRkcyvpvg vf orggre guna vzcyvpvg.\nFvzcyr vf orggre guna pbzcyrk.\nPbzcyrk vf orggre guna pbzcyvpngrq.\nSyng vf orggre guna arfgrq.\nFcnefr vf orggre guna qrafr.\nErnqnovyvgl pbhagf.\nFcrpvny pnfrf nera'g fcrpvny rabhtu gb oernx gur ehyrf.\nNygubhtu cenpgvpnyvgl orngf chevgl.\nReebef fubhyq arire cnff fvyragyl.\nHayrff rkcyvpvgyl fvyraprq.\nVa gur snpr bs nzovthvgl, ershfr gur grzcgngvba gb thrff.\nGurer fubhyq or bar-- naq cersrenoyl bayl bar --boivbhf jnl gb qb vg.\nNygubhtu gung jnl znl abg or boivbhf ng svefg hayrff lbh'er Qhgpu.\nAbj vf orggre guna arire.\nNygubhtu arire vf bsgra orggre guna *evtug* abj.\nVs gur vzcyrzragngvba vf uneq gb rkcynva, vg'f n onq vqrn.\nVs gur vzcyrzragngvba vf rnfl gb rkcynva, vg znl or n tbbq vqrn.\nAnzrfcnprf ner bar ubaxvat terng vqrn -- yrg'f qb zber bs gubfr!"
>>> id(this.s)
94337390100336
>>> hex(id(this.s))
'0x55cca2a03f70'
>>> hex(hash(this.s))
'-0x44bd24ea1130903a'
>>> id(this.s)
94337390100336
>>> id('hello')
139836335465776
>>> id('hello')
139836335603440
>>> hash('hello')
-5903669055829208072
>>> hash('hello')
-5903669055829208072
>>> hash(this.s)
-4953155752906756154
>>> import hashlib
>>> hashlib.sha1
<function _hashlib.openssl_sha1>
>>> hashlib.sha1('hello')
>>> hashlib.sha1(b'hello')
<sha1 HASH object @ 0x7f2e2e477fc0>
>>> hashlib.sha1(b'hello').digest()
b'\xaa\xf4\xc6\x1d\xdc\xc5\xe8\xa2\xda\xbe\xde\x0f;H,\xd9\xae\xa9CM'
>>> int(hashlib.sha1(b'hello').digest())
>>> hashlib.sha128(b'hello')
>>> hasher = hashlib.md5()
>>> hasher = hashlib.md5(64)
>>> hasher = hashlib.md5()
>>> hasher.update('hello')
>>> hasher.update(b'hello')
>>> hasher.digest()
b']A@*\xbcK*v\xb9q\x9d\x91\x10\x17\xc5\x92'
>>> hasher(b'hello').digest()
>>> hashlib.md5('hello')
>>> hashlib.md5(b'hello')
<md5 HASH object @ 0x7f2e2e367c90>
>>> hashlib.md5(b'hello').digest()
b']A@*\xbcK*v\xb9q\x9d\x91\x10\x17\xc5\x92'
>>> hashlib.sha256(b'hello').digest()
b',\xf2M\xba_\xb0\xa3\x0e&\xe8;*\xc5\xb9\xe2\x9e\x1b\x16\x1e\\\x1f\xa7B^s\x043b\x93\x8b\x98$'
>>> [ord(c) for c in hashlib.sha256(b'hello').digest()]
>>> [c for c in hashlib.sha256(b'hello').digest()]
[44,
 242,
 77,
 186,
 95,
 176,
 163,
 14,
 38,
 232,
 59,
 42,
 197,
 185,
 226,
 158,
 27,
 22,
 30,
 92,
 31,
 167,
 66,
 94,
 115,
 4,
 51,
 98,
 147,
 139,
 152,
 36]
>>> sum([c * 256**i for i, c in enumerate(hashlib.sha1(b'hi').digest())])
379176612637934530949874122401510109001170234306
>>> sum([c * 256**i for i, c in enumerate(hashlib.sha256(b'hi').digest())])
74395213546846681896619874105760563318600540128735329642495709678480075735951
>>> from hashlib import *
>>> len(sha1(b'hi').digest())
20
>>> len(sha256(b'hi').digest())
32
>>> len(sha512(b'hi').digest())
64
>>> len(md5(b'hi').digest())
16
>>> sum([c * 256**i for i, c in enumerate(md5(b'hi').digest())])
79733582137966110545874937074290456137
>>> 16 * 8
128
>>> len(sha512(b'hi').digest()) * 8
512
>>> hasher = sha256()
>>> hasher.update('hello')
>>> hasher.update(b'hello')
>>> hasher.update(b'world')
>>> hasher.digest() == md5(b'helloworld')
False
>>> hasher.digest()
b'\x93j\x18\\\xaa\xa2f\xbb\x9c\xbe\x98\x1e\x9e\x05\xcbx\xcds+\x0b2\x80\xeb\x94D\x12\xbbo\x8f\x8f\x07\xaf'
>>> hasher = md5()
>>> hasher.update(b'hello')
>>> hasher.digest()
b']A@*\xbcK*v\xb9q\x9d\x91\x10\x17\xc5\x92'
>>> hasher.update(b'world')
>>> hasher.digest()
b'\xfc^\x03\x8d8\xa5p2\x08TA\xe7\xfep\x10\xb0'
>>> hasher = md5()
>>> hasher.update(b'helloworld')
>>> hasher.digest()
b'\xfc^\x03\x8d8\xa5p2\x08TA\xe7\xfep\x10\xb0'
>>> md5(b'helloworld')
<md5 HASH object @ 0x7f2e2e3bbf60>
>>> md5(b'helloworld').digest()
b'\xfc^\x03\x8d8\xa5p2\x08TA\xe7\xfep\x10\xb0'
```


What are some short 8-byte hashes I could use.  And can I compute the integer representation without using sum() on a generator?

```python
>>> from hashlib import md5
>>> len(md5(b'hi').digest())
16
>>> int.from_bytes(md5(b'hi').digest(), byteorder='big', signed=False)
98313755022045530244343041484663159867
>>> int.from_bytes(md5(b'hi').digest(), byteorder='little', signed=False)
79733582137966110545874937074290456137
>>> (2**8)**16
340282366920938463463374607431768211456
```

Back to hashlib

```python
>>> import hashlib
>>> int.from_bytes(hashlib.sha1(b'hi').digest(), byteorder='little', signed=False)
379176612637934530949874122401510109001170234306
>>> len(hashlib.sha1(b'hi').digest())
20

What about zlib...

```python
>>> import zlib
>>> len(zlib.adler32(b'barackobama'))
>>> zlib.adler32(b'barackobama')
442303589
>>> zlib.adler32(b'b')
6488163
>>> zlib.adler32(b'a')
6422626
>>> zlib.adler32(b'q')
7471218
>>> zlib.adler32(0)
# ValueError only bytes allowed
>>> zlib.adler32(b'0')
3211313
```

Let's try all the available open ssl algorithms in hashlib:

```python
>>> hashlib.sha224().digest_size
28
>>> hashlib.algorithms_available
{'blake2b',
 'blake2s',
 'md5',
 'sha1',
 'sha224',
 'sha256',
 'sha384',
 'sha3_224',
 'sha3_256',
 'sha3_384',
 'sha3_512',
 'sha512',
 'shake_128',
 'shake_256'}
>>> hashlib.blake2b().digest_size
64
>>> hashlib.blake2s().digest_size
32
>>> [hashlib.new(name).digest_size for name in hashlib.algorithms_available]
[32, 48, 64, 28, 20, 32, 64, 28, 48, 16, 0, 64, 32, 0]
>>> len(hashlib.sha1(b'hi').digest())
20
>>> len(hashlib.md5(b'hi').digest())
16
```

Shake and bake:

```python
>>> len(hashlib.shake_128(b'hi').digest(8))
8
>>> len(hashlib.shake_128(b'hi').digest(16))
16
>>> len(hashlib.shake_128(b'hi').digest(8))
8
```
