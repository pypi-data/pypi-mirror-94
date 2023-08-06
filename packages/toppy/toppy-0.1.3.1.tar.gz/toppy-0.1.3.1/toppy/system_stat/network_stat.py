import re
import time
from collections import namedtuple

import psutil

netstat = namedtuple('netstat', 'rx tx')

def make_netstat(old_stats, new_stats, timediff):
    rx = (new_stats.bytes_recv - old_stats.bytes_recv) / timediff
    tx = (new_stats.bytes_sent - old_stats.bytes_sent) / timediff
    return netstat(rx, tx)

def is_valid_device(name, stat):
    if not re.fullmatch(r"en\d+|enp\d+s\d|wlp\d+s\d+f\d+", name):
        return False
    if stat.bytes_recv == 0 and stat.bytes_sent == 0:
        return False
    return True

class NetworkStat:
    def __init__(self):
        self._stats = None
        self._time = None

        self.keys = None
        self.stats = None

    def setup(self):
        self._update()
        self.keys = sorted(self._stats.keys())

    def update(self):
        old_stats, old_time = self._stats, self._time
        self._update()
        new_stats, new_time = self._stats, self._time
        timediff_s = new_time - old_time

        keys = set(old_stats.keys()) & set(new_stats.keys())
        self.stats = {
            key: make_netstat(old_stats[key], new_stats[key], timediff_s) for key in keys
        }

    def _update(self):
        self._stats = {
            k: v for k, v in psutil.net_io_counters(pernic=True).items() if is_valid_device(k, v)
        }
        self._time = time.time()
