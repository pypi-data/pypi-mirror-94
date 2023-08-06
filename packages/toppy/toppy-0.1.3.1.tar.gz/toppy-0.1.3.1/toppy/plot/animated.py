import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


class AnimatedAxes:
    def setup(self, axes, x):
        raise NotImplementedError(f'Please implement {self.__class__.__name__}.setup(axes, x)')

    def update(self):
        raise NotImplementedError(f'Please implement {self.__class__.__name__}.update()')


class AnimatedFigure:
    def __init__(self, animated_axes, update_interval, display_seconds, fig=None):
        self.animated_axes = animated_axes
        self.update_interval = update_interval
        self.display_seconds = display_seconds
        self.fig = fig or plt.figure()
        self.setup_actors = None

    def run(self, block=True):
        self.anim = animation.FuncAnimation(
            self.fig,
            self.update,
            init_func=self.setup,
            interval=self.update_interval * 1000,
            save_count=1,
            cache_frame_data=False,
            blit=True
        )
        plt.show(block=block)

    def setup(self):
        self.setup_actors = self.setup_actors or list(self._setup_animated_axes())
        return self.setup_actors

    def _setup_animated_axes(self):
        x = np.arange(0, -self.display_seconds, -self.update_interval)[::-1]
        axes = tolist(self.fig.subplots(len(self.animated_axes), 1))
        for animated_axes, axes in zip(self.animated_axes, axes):
            yield from tolist(animated_axes.setup(axes, x))

    def update(self, frame):
        actors = list(self._update_animated_axes())
        return actors

    def _update_animated_axes(self):
        for animated_axes in self.animated_axes:
            yield from tolist(animated_axes.update())


def tolist(obj):
    if type(obj) in (list, np.ndarray):
        return obj
    return [obj]
