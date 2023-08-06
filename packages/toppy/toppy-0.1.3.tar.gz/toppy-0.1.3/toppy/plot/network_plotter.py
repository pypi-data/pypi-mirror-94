import math

import numpy as np

from ..system_stat import NetworkStat
from . import common
from .animated import AnimatedAxes


class NetworkPlotter(AnimatedAxes):
    def __init__(self, keys=None, net=None):
        self.net = net or NetworkStat()
        self.keys = keys
        self.ylim = 1024

    def setup(self, axes, x):
        self.axes = axes
        self.net.setup()
        self.keys = self.keys or self.net.keys
        self.labels = []
        for key in self.keys:
            self.labels += [f'{key} RX', f'{key} TX']
        self.ys = [common.none_array(x.size) for _ in self.labels]
        self.lines = [axes.plot(x, y, label=label)[0] for label, y in zip(self.labels, self.ys)]

        axes.set_title('Network')
        axes.set_ylabel('Network IO')
        axes.set_xlim(x.min(), x.max())
        axes.set_ylim(0, self.ylim)
        axes.tick_params('x', bottom=False, labelbottom=False)
        axes.grid(True, axis='y')
        axes.legend()

        return self.lines

    def update(self):
        self.net.update()

        for label, y, line in zip(self.labels, self.ys, self.lines):
            key, direction = label.split()
            v = self.net.stats[key].rx if direction == 'RX' else self.net.stats[key].tx
            common.additem_cyclic_inplace(y, v)

            line.set_ydata(y)

        self._update_ylim()
        return self.lines

    def _update_ylim(self):
        ymax = 1024
        for y in self.ys:
            if y[-1] != None:
                ymax = max(ymax, y[y!=None].max())
        ylim = 4 ** math.ceil(log4(ymax))
        if self.ylim != ylim:
            self.ylim = ylim
            self.axes.set_ylim(0, self.ylim)
            self.axes.figure.canvas.resize_event()

def log4(x):
    return math.log2(x) / 2
