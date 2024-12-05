"""pyfina tools and base class"""

from __future__ import annotations
import logging
import math
import os
import struct

from typing import Literal

import numpy as np

logging.basicConfig()
pyfina_logger = logging.getLogger(__name__)


def trim(feed_id: int, data_dir: str, limit: int = 100) -> None:
    """
    checks and removes anomalies (values above a threshold limit, eg 100)
    feed_id: feed number
    data_dir: feed path (eg /var/opt/emoncms/phpfina)
    limit: threshold we don't want to exceed
    """
    meta = getMeta(feed_id, data_dir)
    if not meta:
        return
    pos = 0
    i = 0
    nbn = 0
    with open(f"{data_dir}/{feed_id}.dat", "rb+") as ts:
        while pos <= meta["npoints"]:
            ts.seek(pos * 4, 0)
            hexa = ts.read(4)
            aa = bytearray(hexa)
            if len(aa) == 4:
                value = struct.unpack("<f", aa)[0]
                if math.isnan(value):
                    nbn += 1
                elif value > limit:
                    message = f"anomaly detected at {pos} : {value}"
                    pyfina_logger.debug(message)
                    i += 1
                    nv = struct.pack("<f", float("nan"))
                    try:
                        ts.seek(pos * 4, 0)
                        ts.write(nv)
                    except Exception as e:
                        pyfina_logger.error(e)
                    finally:
                        pyfina_logger.debug("4 bytes written")
            pos += 1
        message = f"{i} anomaly(ies)"
        pyfina_logger.debug(message)
        message = f"{nbn} nan"
        pyfina_logger.debug(message)


def getMeta(feed_id: int, data_dir: str) -> Literal[False] | dict[str, int]:
    """
    decoding the .meta file
    feed_id (4 bytes, Unsigned integer)
    npoints (4 bytes, Unsigned integer, Legacy : use instead filesize//4 )
    interval (4 bytes, Unsigned integer)
    start_time (4 bytes, Unsigned integer)
    Returns:
        dict with keys: interval, start_time, npoints, end_time
        where end_time is the timestamp of the last data point
    """
    with open(f"{data_dir}/{feed_id}.meta", "rb") as f:
        f.seek(8, 0)
        hexa = f.read(8)
        aa = bytearray(hexa)
        if len(aa) == 8:
            decoded = struct.unpack("<2I", aa)
        else:
            pyfina_logger.error("corrupted meta - aborting")
            return False
    meta = {
        "interval": decoded[0],
        "start_time": decoded[1],
        "npoints": os.path.getsize(f"{data_dir}/{feed_id}.dat") // 4,
    }
    meta['end_time'] = meta['start_time'] + (meta['npoints'] * meta['interval']) - meta['interval']
    return meta

class PyFina(np.ndarray):
    """pyfina class."""
    start: int | None = None
    step: int | None = None
    nb_nan: int | None = None
    first_non_nan_value: float | None = None
    first_non_nan_index: int | None = None
    starting_by_nan : bool | None = None

    def __new__(
        cls,
        feed_id: int,
        data_dir: str,
        start: int,
        step: int,
        npts: int,
        **kwargs
    ):
        remove_nan: bool = kwargs.get("remove_nan", True)
        meta = getMeta(feed_id, data_dir)
        if not meta:
            return None
        # decoding and sampling the .dat file
        # values are 32 bit floats, stored on 4 bytes
        # to estimate value(time), position in the dat file is calculated as follow :
        # pos = (time - meta["start_time"]) // meta["interval"]
        # Nota : if remove_nan is True and a NAN is detected, the algorithm takes previous value
        obj = super().__new__(cls, shape=(npts,))
        obj.fill(np.nan)
        raw_obj = np.empty(npts)
        raw_obj.fill(np.nan)
        pyfina_logger.debug(obj)
        end = start + (npts - 1) * step
        time = start
        i = 0
        nb_nan = 0
        # Avoid Reading file if time >= end_time
        if time >= meta['end_time']:
            raise ValueError("Error: invalid start value, start must be less than end time value "
                             "defined by start_time + (npoints * interval) from meta."
                            )
        with open(f"{data_dir}/{feed_id}.dat", "rb") as ts:
            while time < end:
                time = start + step * i
                pos = (time - meta["start_time"]) // meta["interval"]
                if 0 <= pos < meta["npoints"]:
                    try:
                        # message = f"trying to find point {i} going to index {pos}"
                        # pyfina_logger.debug(message)
                        ts.seek(pos * 4, 0)
                        hexa = ts.read(4)
                        aa = bytearray(hexa)
                    except Exception as e:
                        message = f"error during file operation {e}"
                        pyfina_logger.error(message)
                    else:
                        if len(aa) == 4:
                            value = struct.unpack("<f", aa)[0]
                            obj[i] = value
                            raw_obj[i] = value
                            if remove_nan and np.isnan(value):
                                nb_nan += 1
                                obj[i] = obj[i - 1]
                        else:
                            message = f"unpacking problem {i} len is {len(aa)} position is {pos}"
                            pyfina_logger.error(message)
                # End reading loop if pos out of bounds
                else:
                    break
                i += 1
        first_non_nan_value = -1
        first_non_nan_index = -1
        starting_by_nan = np.isnan(raw_obj[0])
        if nb_nan < npts:
            finiteness_obj = np.isfinite(raw_obj)
            if finiteness_obj.sum() > 0:
                first_non_nan_index = np.where(finiteness_obj)[0][0]
                first_non_nan_value = raw_obj[finiteness_obj][0]
                if starting_by_nan and remove_nan:
                    obj[:first_non_nan_index] = (
                        np.ones(first_non_nan_index) * first_non_nan_value
                    )
        # storing the "signature" of the "sampled" feed
        obj.start = start
        obj.step = step
        obj.nb_nan = nb_nan
        obj.first_non_nan_value = first_non_nan_value
        obj.first_non_nan_index = first_non_nan_index
        obj.starting_by_nan = starting_by_nan
        return obj

    def timescale(self):
        """
        return the time scale of the feed as a numpy array
        """
        return np.arange(0, self.step * self.shape[0], self.step)
