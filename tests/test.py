"""test : open feed and plot image."""

import datetime
import os
import time
import matplotlib
import matplotlib.pyplot as plt
from multigraph import check_starting_nan
from PyFina import getMeta, PyFina

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

STEP = 3600

def generate_episode(feed_nb: int, feed_name: str, feed_unit: str, **kwargs):
    """visualize initial episode."""
    meta = getMeta(feed_nb, DATA_DIR)
    print(meta)
    # start
    start = kwargs.get("start", meta["start_time"])

    # length to display in seconds
    length = meta["npoints"] * meta["interval"]
    if not kwargs.get("view_whole", False):
        length = min(length, 8 * 24 * 3600)
    length = kwargs.get("seconds", length)
    print(length)

    # step
    use_original_step = kwargs.get("use_original_step", False)
    step = meta["interval"] if use_original_step else STEP

    datas = PyFina(feed_nb, DATA_DIR, start, step, length // step)
    check_starting_nan(feed_name, datas)
    localstart = datetime.datetime.fromtimestamp(start)
    utcstart = datetime.datetime.fromtimestamp(start, datetime.timezone.utc)
    title = f"starting on :\nUTC {utcstart}\n{time.tzname[0]} {localstart}"
    figure = plt.figure(figsize = (10, 10))
    matplotlib.rc('font', size=8)
    plt.subplot(111)
    plt.title(title)
    plt.ylabel(f"{feed_name} - {feed_unit}")
    plt.xlabel("time in hours")
    plt.plot(datas)
    figure.savefig(f"nb_{feed_nb}_{feed_name}.png")
    if os.environ.get('DISPLAY_PLOTS', '').lower() == 'true':
        plt.show()

if __name__ == "__main__":
    generate_episode(1, "température extérieure", "°C")
    generate_episode(
        2,
        "mano8 recordings whole",
        "°C",
        view_whole=True
    )
    generate_episode(
        2,
        "mano8 recordings",
        "°C",
        start=1540166400 - 3600 * 24,
        seconds=24 * 3600
    )
