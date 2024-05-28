"""test : open feed and plot image."""

import datetime
import matplotlib
import matplotlib.pylab as plt
from PyFina import getMeta, PyFina
import time
import urllib.request as request

feed_nb = 1

def retrieve(feed_nb,extension):
    file_name = f"{feed_nb}.{extension}"
    url = f"https://raw.githubusercontent.com/Open-Building-Management/PyFina/master/tests/datas/{file_name}"
    request.urlretrieve(url, file_name)
print("downloading some datas for testing....")
retrieve(feed_nb,"dat")
retrieve(feed_nb,"meta")

# feed storage on a standard emoncms server
# dir = "/var/opt/emoncms/phpfina"
dir = "."
meta = getMeta(feed_nb,dir)
print(meta)
step = 3600
start = meta["start_time"]
window = 8*24*3600
length = meta["npoints"] * meta["interval"]
if window > length:
    window = length
nbpts = window // step
Text = PyFina(feed_nb,dir,start,step,nbpts)


localstart = datetime.datetime.fromtimestamp(start)
utcstart = datetime.datetime.utcfromtimestamp(start)
title = f"starting on :\nUTC {utcstart}\n{time.tzname[0]} {localstart}"
figure = plt.figure(figsize = (10, 10))
matplotlib.rc('font', size=8)
plt.subplot(111)
plt.title(title)
plt.ylabel("outdoor Temp °C")
plt.xlabel("time in hours")
plt.plot(Text)
figure.savefig(f"feed_{feed_nb}.png")
