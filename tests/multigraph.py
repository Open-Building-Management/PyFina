"""produces some snapshots opening the bloch dataset."""

import datetime
import random
import time

import matplotlib
import matplotlib.pylab as plt
from PyFina import getMeta, PyFina

# télécharger le fichier contenant les données de Marc Bloch 2021
# puis lancer tar -xvf pour décompresser
dir = "phpfina"
feeds = {
    "Text" : 5,
    "TziqNord": 8,
    "TtecNord": 11,
    "TdepNord": 21,
    "TretNord": 22,
    "pompeNord": 23
}
step = 3600
verbose = False
# episode length : 8 days !!
episode_length = 8 * 24 * 3600

def analyse():
    """
    étant donné un dictionnaire de numéros de flux
    calcule les timestamps de départ et de fin communs à cet ensemble de flux
    """
    starts = []
    ends = []
    for f in feeds:
        meta = getMeta(feeds[f], dir)
        if verbose:
            print(meta)
        start = meta["start_time"]
        length = meta["npoints"] * meta["interval"]
        end = start + length
        starts.append(start)
        ends.append(end)
    start = max(starts)
    end = min(ends)
    length = end - start
    nbpts = episode_length // step
    if episode_length > length:
        nbpts = length // step
    return start, end, nbpts

start, end, nbpts = analyse()

def check_starting_nan(feed):
    """check if feed is starting by nan"""
    if feed.starting_by_nan:
        print(f"first non nan value {feed.first_non_nan_value}")
        print(f"at index {feed.first_non_nan_index}")

def generate_episode(start_ts):
    """
    permet de visualiser un épisode commencant à start_ts
    """
    temp_ext = PyFina(feeds["Text"], dir, start_ts, step, nbpts)
    temp_ziq_nord = PyFina(feeds["TziqNord"], dir, start_ts, step, nbpts)
    temp_tec_nord = PyFina(feeds["TtecNord"], dir, start_ts, step, nbpts)
    temp_dep_nord = PyFina(feeds["TdepNord"], dir, start_ts, step, nbpts)
    temp_ret_nord = PyFina(feeds["TretNord"], dir, start_ts, step, nbpts)
    all_feeds = (
        temp_ext,
        temp_ziq_nord,
        temp_tec_nord,
        temp_dep_nord,
        temp_ret_nord
    )
    for feed in all_feeds:
        check_starting_nan(feed)
    localstart = datetime.datetime.fromtimestamp(start_ts)
    utcstart = datetime.datetime.utcfromtimestamp(start_ts)
    title = f"starting on : UTC {utcstart}\n{time.tzname[0]} {localstart}"
    figure = plt.figure(figsize = (20, 10))
    matplotlib.rc('font', size=8)
    ax1 = plt.subplot(211)
    plt.title(title)
    plt.ylabel("outdoor Temp °C")
    plt.xlabel("time in hours")
    plt.plot(temp_ext, label="Text")
    plt.legend(loc='upper left')
    ax1 = ax1.twinx()
    plt.ylabel("indoor Temp °C")
    plt.plot(temp_ziq_nord, label = "TziqNord", color="green")
    plt.plot(temp_tec_nord, label = "TtecNord",  color="orange")
    plt.legend(loc='upper right')
    plt.subplot(212, sharex=ax1)
    plt.ylabel("hot water Temp °C")
    plt.plot(temp_dep_nord, label = "TdepNord")
    plt.plot(temp_ret_nord, label = "TretNord")
    plt.legend(loc='upper right')
    figure.savefig(f"bloch_{start_ts}.png")

if end - episode_length > start :
    for _ in range(10):
        start_ts = random.randrange(start, end - episode_length)
        generate_episode(start_ts)
else :
    generate_episode(start)
