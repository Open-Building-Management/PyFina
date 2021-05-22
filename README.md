# PyFina

PyFina is a subclass of numpy np.ndarray to import emoncms PHPFINA feeds as numpy arrays

## Installation

```
python3 -m pip install PyFina
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
To plot the first 8 days of datas, with a sampling interval of 3600 s :

```
step = 3600
start = meta["start_time"]
window = 8*24*3600
length = meta["npoints"] * meta["interval"]
if window > length:
    window = length
nbpts = window // step
Text = PyFina(1,dir,start,step,nbpts)
plt.subplot(111)
plt.plot(Text)
plt.show()

```
