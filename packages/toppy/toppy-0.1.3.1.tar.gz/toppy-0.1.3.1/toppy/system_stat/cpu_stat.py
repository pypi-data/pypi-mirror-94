import psutil


class CPUStat:
    def __init__(self):
        self.user = None
        self.nice = None
        self.system = None
        self.idle = None
        self.utilization = None


    def setup(self):
        self._update()

    def update(self):
        self._update()

    def _update(self):
        stat = psutil.cpu_times_percent()
        self.user = stat.user
        self.nice = stat.nice
        self.system = stat.system
        self.idle = stat.idle
        self.utilization = 100 - stat.idle
