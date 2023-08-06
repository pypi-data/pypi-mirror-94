import argparse
import math
import sys
import time
from dataclasses import dataclass
from typing import List, Type

import matplotlib.pyplot as plt
import numpy as np

from .plot import (AnimatedFigure, CPUPlotter, GPUPlotter, IOPlotter,
                   MemoryPlotter, NetworkPlotter)

if sys.platform == 'linux':
    DEFAULT_PLOTTER_CLASSES = (CPUPlotter, GPUPlotter, MemoryPlotter, IOPlotter, NetworkPlotter)
else:
    DEFAULT_PLOTTER_CLASSES = (CPUPlotter, MemoryPlotter, IOPlotter, NetworkPlotter)

@dataclass
class ToppyArgs:
    update_interval: float = 1.0
    display_seconds: float = 60.0
    plotter_classes: list = DEFAULT_PLOTTER_CLASSES

    @classmethod
    def parse_args(cls, args=None):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--update-interval', type=float,
                            help='update interval ( >= 0.01 )')
        parser.add_argument('-s', '--display_seconds', type=float,
                            help='number of seconds to show ( >= 1 )')
        args = parser.parse_args(args)
        if not cls._validate_args(args):
            parser.print_usage()
            parser.exit()
        present_args = {k: v for k, v in args.__dict__.items() if v is not None}
        return cls(**present_args)

    @staticmethod
    def _validate_args(args):
        if args.update_interval is not None and args.update_interval < 0.01: return False
        if args.display_seconds is not None and args.display_seconds < 1: return False
        return True



class Toppy:
    def __init__(self, args: ToppyArgs = None):
        self.args = args or ToppyArgs()

    def run(self, block=True):
        plotters = [plotter_cls() for plotter_cls in self.args.plotter_classes]
        fig = plt.figure('Toppy')
        animated_figure = AnimatedFigure(
            plotters,
            self.args.update_interval,
            self.args.display_seconds,
            fig
        )
        animated_figure.run(block=block)
