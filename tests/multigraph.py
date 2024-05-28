"""produces some snapshots opening the bloch dataset."""

import datetime
import random
import time

import matplotlib
import matplotlib.pylab as plt
from PyFina import getMeta, PyFina

# télécharger le fichier contenant les données de Marc Bloch 2021
# puis lancer tar -xvf pour décompresser
DATA_DIR = "phpfina"
feeds = {
    "Text" : 5,
    "TziqNord": 8,
    "TtecNord": 11,
    "TdepNord": 21,
    "TretNord": 22,
    "pompeNord": 23
}
STEP = 3600
VERBOSE = False
# episode length : 8 days !!
EPISODE_LENGTH = 8 * 24 * 3600

def analyse():
    """
    étant donné un dictionnaire de numéros de flux
    calcule les timestamps de départ et de fin communs à cet ensemble de flux
    """
    starts = []
    ends = []
    for _, feed_nb in feeds.items():
        meta = getMeta(feed_nb, DATA_DIR)
        if VERBOSE:
            print(meta)
        start = meta["start_time"]
        length = meta["npoints"] * meta["interval"]
        end = start + length
        starts.append(start)
        ends.append(end)
    start = max(starts)
    end = min(ends)
    length = end - start
    nbpts = EPISODE_LENGTH // STEP
    if EPISODE_LENGTH > length:
        nbpts = length // STEP
    return start, end, nbpts

def check_starting_nan(feed_name, feed):
    """check if feed is starting by nan"""
    print(f"{feed_name} : {feed.nb_nan} nan in the feed")
    if feed.starting_by_nan:
        message = f"first non nan value {feed.first_non_nan_value}"
        message = f"{message} at index {feed.first_non_nan_index}"
        print(message)

def generate_episode(start_ts, nbpts):
    """visualise un épisode commencant à start_ts"""
    temp_ext = PyFina(feeds["Text"], DATA_DIR, start_ts, STEP, nbpts)
    temp_ziq_nord = PyFina(feeds["TziqNord"], DATA_DIR, start_ts, STEP, nbpts)
    temp_tec_nord = PyFina(feeds["TtecNord"], DATA_DIR, start_ts, STEP, nbpts)
    temp_dep_nord = PyFina(feeds["TdepNord"], DATA_DIR, start_ts, STEP, nbpts)
    temp_ret_nord = PyFina(feeds["TretNord"], DATA_DIR, start_ts, STEP, nbpts)
    feed_objects = {
        "Text": temp_ext,
        "TziqNord": temp_ziq_nord,
        "TtecNord": temp_tec_nord,
        "TdepNord": temp_dep_nord,
        "TretNord": temp_ret_nord
    }
    for feed_name, feed_object in feed_objects.items():
        check_starting_nan(feed_name, feed_object)
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


if __name__ == "__main__":
    common_start, common_end, common_nbpts = analyse()

    if (common_end - EPISODE_LENGTH) > common_start :
        for _ in range(10):
            start_ts_ep = random.randrange(common_start, common_end - EPISODE_LENGTH)
            print(start_ts_ep)
            generate_episode(start_ts_ep, common_nbpts)
    else :
        print(common_start)
    generate_episode(common_start, common_nbpts)
