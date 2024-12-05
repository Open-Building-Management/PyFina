"""test : open feed and plot image."""

import datetime
import os
import time
import matplotlib
import matplotlib.pyplot as plt
from multigraph import check_starting_nan
from PyFina import getMeta, PyFina

FEED_NB = 1
DATA_DIR = os.path.join(
    os.path.abspath(os.getcwd()),
    "datas"
)
if not os.path.isdir(DATA_DIR):
    DATA_DIR = os.path.join(
        os.path.abspath(os.getcwd()),
        "tests",
        "datas"
    )
    if not os.path.isdir(DATA_DIR):
        raise FileNotFoundError(f"Could not find data directory in any location: {DATA_DIR}")

meta = getMeta(FEED_NB, DATA_DIR)
print(meta)
STEP = 3600
start = meta["start_time"]
length = meta["npoints"] * meta["interval"]
WINDOW = min(8 * 24 * 3600, length)

nbpts = WINDOW // STEP
temp_ext = PyFina(FEED_NB, DATA_DIR, start, STEP, nbpts)

check_starting_nan("température extérieure", temp_ext)

localstart = datetime.datetime.fromtimestamp(start)
utcstart = datetime.datetime.fromtimestamp(start, datetime.timezone.utc)
title = f"starting on :\nUTC {utcstart}\n{time.tzname[0]} {localstart}"
figure = plt.figure(figsize = (10, 10))
matplotlib.rc('font', size=8)
plt.subplot(111)
plt.title(title)
plt.ylabel("outdoor Temp °C")
plt.xlabel("time in hours")
plt.plot(temp_ext)
figure.savefig(f"feed_{FEED_NB}.png")
if os.environ.get('DISPLAY_PLOTS', '').lower() == 'true':
    plt.show()
