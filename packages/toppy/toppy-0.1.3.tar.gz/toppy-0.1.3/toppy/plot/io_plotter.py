import numpy as np

from ..system_stat import IOStat
from . import common
from .animated import AnimatedAxes


class IOPlotter(AnimatedAxes):
    def __init__(self, keys=None, io=None):
        self.io = io or IOStat()
        self.keys = keys

    def setup(self, axes, x):
        self.io.setup()
        self.keys = self.keys or self.io.keys
        self.ys = [common.none_array(x.size) for _ in self.keys]
        self.lines = [axes.plot(x, y, label=key)[0] for key, y in zip(self.keys,self.ys)]

        axes.set_title('IO')
        axes.set_ylabel('% IO time')
        axes.set_xlim(x.min(), x.max())
        axes.set_ylim(0, 100)
        axes.tick_params('x', bottom=False, labelbottom=False)
        axes.grid(True, axis='y')
        axes.legend()

        return self.lines

    def update(self):
        self.io.update()

        for key, y, line in zip(self.keys, self.ys, self.lines):
            common.additem_cyclic_inplace(y, self.io.stats[key].busy_time)

            line.set_ydata(y)

        return self.lines
