import psutil


class MemoryStat:
    def __init__(self):
        self.mem = None
        self.swap = None

    def setup(self):
        self._update()

    def update(self):
        self._update()

    def _update(self):
        self.mem = psutil.virtual_memory()
        self.swap = psutil.swap_memory()
