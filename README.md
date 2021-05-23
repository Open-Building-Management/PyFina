# PyFina

PyFina is a subclass of numpy np.ndarray to import emoncms PHPFINA feeds as numpy arrays

## Installation

```
python3 -m pip install PyFina
```
or, for python on Windows
```
py -m pip install PyFina
```

## Post installation testing

copy the content of [test.py](https://raw.githubusercontent.com/Open-Building-Management/PyFina/main/tests/test.py), paste it in a blank file on your local machine and save it using the same name.

```
py test.py
```

## Getting Started

To retrieve metadatas for feed number 1 :

```
from PyFina import getMeta, PyFina
import matplotlib.pylab as plt

dir = "/var/opt/emoncms/phpfina"
meta = getMeta(1,dir)
print(meta)
```
To import the first 8 days of datas, with a sampling interval of 3600 s :

```
step = 3600
start = meta["start_time"]
window = 8*24*3600
length = meta["npoints"] * meta["interval"]
if window > length:
    window = length
nbpts = window // step
Text = PyFina(1,dir,start,step,nbpts)
```
To plot:
```
plt.subplot(111)
plt.plot(Text)
plt.show()
```
With the above code, the xrange will be expressed in hour, so 192 points will be displayed

![](test.png)

If you want to express the xrange in seconds :
```
xrange = Text.timescale()
plt.subplot(111)
plt.plot(xrange,Text)
plt.show()
```
To catch the signature of the created PyFina object :
```
print(Text.start)
print(Text.step)
```
