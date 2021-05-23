# PyFina

PyFina is a subclass of numpy np.ndarray to import emoncms PHPFINA feeds as numpy arrays

The pip installer will install any missing requirements (numpy, matplotlib) 

PyFina brings the power of numpy to the PHPFINA timeseries, including basic operations and more : 
addition, soustraction, multiplication, division, min, max, mean, sum, slicing with the bracket operator

Note : any operation on a PyFina object results to a standard numpy nd.array object. 
The signature of the PyFina object is lost.

It does not prevent to add two PyFina objects of the same size but sampled with different intervals


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
# classic emoncms feed storage on linux
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
To catch the signature of the created PyFina object :
```
print(Text.start)
print(Text.step)
```

To plot:
```
plt.subplot(111)
plt.ylabel("outdoor Temp °C")
plt.xlabel("time in hours")
plt.plot(Text)
plt.show()
```
With the above code, the xrange will be expressed in hour, so 192 points will be displayed

![](test.png)

To express the xrange in seconds :
```
xrange = Text.timescale()
plt.subplot(111)
plt.plot(xrange,Text)
plt.show()
```

