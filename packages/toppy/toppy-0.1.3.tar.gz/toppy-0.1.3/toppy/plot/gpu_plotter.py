import numpy as np

from ..system_stat import GPUStat
from . import common
from .animated import AnimatedAxes


class GPUPlotter(AnimatedAxes):
    def __init__(self, gpu=None):
        self.gpu = gpu or GPUStat()

    def setup(self, axes, x):
        self.gpu.setup()

        self.ys = [common.none_array(x.size) for _ in self.gpu.gpus]

        axes.set_title('GPU')
        axes.set_ylabel('% GPU')
        axes.set_xlim(x.min(), x.max())
        axes.set_ylim(0, 100)
        axes.tick_params('x', bottom=False, labelbottom=False)
        axes.grid(True, axis='y')

        self.lines = [
            axes.plot(x, y, label=gpu)[0] for y, gpu in zip(self.ys, self.gpu.gpus)
        ]
        axes.legend()
        return self.lines

    def update(self):
        self.gpu.update()

        for y, utilization, line in zip(self.ys, self.gpu.utilizations, self.lines):
            common.additem_cyclic_inplace(y, utilization)
            line.set_ydata(y)
        return self.lines
