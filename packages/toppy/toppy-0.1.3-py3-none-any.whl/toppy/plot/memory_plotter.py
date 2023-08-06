import numpy as np

from ..system_stat import MemoryStat
from . import common
from .animated import AnimatedAxes


class MemoryPlotter(AnimatedAxes):
    def __init__(self, mem=None):
        self.mem = mem or MemoryStat()

    def setup(self, axes, x):
        self.mem.setup()
        self.y_mem = common.none_array(x.size)
        self.y_swap = common.none_array(x.size)
        self.line_mem = axes.plot(x, self.y_mem, label='Memory')[0]
        self.line_swap = axes.plot(x, self.y_swap, label='Swap')[0]
        self.lines = [self.line_mem, self.line_swap]

        axes.set_title('Memory')
        axes.set_ylabel('% Memory')
        axes.set_xlim(x.min(), x.max())
        axes.set_ylim(0, 100)
        axes.tick_params('x', bottom=False, labelbottom=False)
        axes.grid(True, axis='y')
        axes.legend()

        return self.lines

    def update(self):
        self.mem.update()

        common.additem_cyclic_inplace(self.y_mem, self.mem.mem.used * 100 / self.mem.mem.total)
        common.additem_cyclic_inplace(self.y_swap, self.mem.swap.used * 100 / self.mem.swap.total)

        self.line_mem.set_ydata(self.y_mem)
        self.line_swap.set_ydata(self.y_swap)

        return self.lines
