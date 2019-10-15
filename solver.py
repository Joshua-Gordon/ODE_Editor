import collections

class Solver(object):
    def __init__(self):
        self.equations = collections.OrderedDict()
        self.start = 0
        self.stop = 1
        self.step = 1

    def addVar(self, v):
        if v in self.equations:
            return False
        self.equations[v] = '0'
        return True

    def solve(self, progress_cb=None):
        pass
