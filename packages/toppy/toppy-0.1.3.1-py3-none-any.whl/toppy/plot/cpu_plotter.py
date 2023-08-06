import numpy as np

from ..system_stat import CPUStat
from . import common
from .animated import AnimatedAxes


class CPUPlotter(AnimatedAxes):
    def __init__(self, cpu=None):
        self.cpu = cpu or CPUStat()

    def setup(self, axes, x):
        self.cpu.setup()

        self.y = common.none_array(x.size)

        axes.set_title('CPU')
        axes.set_ylabel('% CPU')
        axes.set_xlim(x.min(), x.max())
        axes.set_ylim(0, 100)
        axes.tick_params('x', bottom=False, labelbottom=False)
        axes.grid(True, axis='y')

        self.line = axes.plot(x, self.y)[0]
        return self.line

    def update(self):
        self.cpu.update()

        common.additem_cyclic_inplace(self.y, self.cpu.utilization)

        self.line.set_ydata(self.y)
        return self.line
