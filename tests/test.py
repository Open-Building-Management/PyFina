from PyFina import getMeta, PyFina
import matplotlib.pylab as plt
import urllib.request as request

feed_nb = 1

def retrieve(feed_nb,extension):
    file_name = "{}.{}".format(feed_nb,extension)
    url = "https://raw.githubusercontent.com/Open-Building-Management/PyFina/master/tests/datas/{}".format(file_name)
    request.urlretrieve(url, file_name)
print("downloading some datas for testing....")
retrieve(feed_nb,"dat")
retrieve(feed_nb,"meta")
input("downloads completed :-) press_any_key")

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
Text = PyFina(1,dir,start,step,nbpts)

import datetime
import time
localstart = datetime.datetime.fromtimestamp(start)
utcstart = datetime.datetime.utcfromtimestamp(start)
title = "starting on :\nUTC {}\n{} {}".format(utcstart,time.tzname[0],localstart)
plt.subplot(111)
plt.title(title)
plt.ylabel("outdoor Temp °C")
plt.xlabel("time in hours")
plt.plot(Text)
plt.show()
