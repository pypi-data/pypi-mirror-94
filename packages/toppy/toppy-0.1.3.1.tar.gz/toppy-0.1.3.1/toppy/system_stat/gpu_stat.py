import re
import subprocess

import gpustat


class GPUStat:
    def __init__(self):
        self.gpus = []
        self.utilizations = []

    def setup(self):
        self.gpus = [gpu.name for gpu in gpustat.new_query()]

    def update(self):
        self.utilizations = [gpu.utilization for gpu in gpustat.new_query()]
