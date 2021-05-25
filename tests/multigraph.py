from PyFina import getMeta, PyFina
import matplotlib.pylab as plt
import datetime
import time
import random

# télécharger le fichier contenant les données de Marc Bloch 2021
# unzip your files in C:/var/opt/emoncms
dir = "C:/var/opt/emoncms/phpfina"
feeds = { "Text" : 5, "TziqNord": 8, "TtecNord": 11, "TdepNord": 21, "TretNord": 22, "pompeNord": 23}
step = 3600
verbose = False
# epL : episode length : 8 days !!
epL = 8*24*3600

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
    nbpts = epL // step
    if epL > length:
        nbpts = length // step
    return start, end, nbpts

start, end, nbpts = analyse()

def viewEpisode(start_ts):
    """
    permet de visualiser un épisode commencant à start_ts
    """
    Text = PyFina(feeds["Text"],dir,start_ts,step,nbpts)
    TziqNord = PyFina(feeds["TziqNord"],dir,start_ts,step,nbpts)
    TtecNord = PyFina(feeds["TtecNord"],dir,start_ts,step,nbpts)
    TdepNord = PyFina(feeds["TdepNord"],dir,start_ts,step,nbpts)
    TretNord = PyFina(feeds["TretNord"],dir,start_ts,step,nbpts)

    localstart = datetime.datetime.fromtimestamp(start_ts)
    utcstart = datetime.datetime.utcfromtimestamp(start_ts)
    title = "starting on : UTC {}\n{} {}".format(utcstart,time.tzname[0],localstart)

    ax1 = plt.subplot(211)
    plt.title(title)
    plt.ylabel("outdoor Temp °C")
    plt.xlabel("time in hours")
    plt.plot(Text, label="Text")
    plt.legend(loc='upper left')
    ax1 = ax1.twinx()
    plt.ylabel("indoor Temp °C")
    plt.plot(TziqNord, label = "TziqNord", color="green")
    plt.plot(TtecNord, label = "TtecNord",  color="orange")
    plt.legend(loc='upper right')
    ax3 = plt.subplot(212, sharex=ax1)
    plt.ylabel("hot water Temp °C")
    plt.plot(TdepNord, label = "TdepNord")
    plt.plot(TretNord, label = "TretNord")
    plt.legend(loc='upper right')
    plt.show()

import signal

class Loop:
    """
    visualisation des épisodes
    """
    def __init__(self):
        self._exit = False

    def run(self):
        """
        boucle
        """
        signal.signal(signal.SIGINT, self._sigint_handler)
        signal.signal(signal.SIGTERM, self._sigint_handler)
        while not self._exit:
            start_ts = random.randrange(start, end - epL)
            viewEpisode(start_ts)

    def _sigint_handler(self, signal, frame):
        """
        Réception du signal de fermeture
        """
        print("signal de fermeture reçu")
        self._exit = True

    def close(self):
        print("fermeture effectuée")

if end - epL > start :
    boucle = Loop()
    boucle.run()
    boucle.close()
else :
    viewEpisode(start)
