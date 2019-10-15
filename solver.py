import collections
from scipy.integrate import solve_ivp
from numpy import *

class Solver(object):
    def __init__(self):
        self.equations = collections.OrderedDict()
        self.conditions = collections.OrderedDict()
        self.start = 0
        self.stop = 1
        self.step = 1

    def addVar(self, v):
        if v in self.equations:
            return False
        self.equations[v] = '0'
        self.conditions[v] = 0
        return True

    def solve(self, progress_cb=None):
        var_unpack = ','.join(list(self.equations.keys()))  + " = Y"
        eq_unpack = "[" + ','.join(list(self.equations.values())) + "]"
        code = """
def model(t,Y):
    {}
    return {}
        """.format(var_unpack,eq_unpack)
        print(code)
        exec(code,globals())
        if progress_cb is not None:
            def report(t,Y):
                progress_cb(Y)
                return True
            solution = solve_ivp(model,[self.start,self.stop],list(self.conditions.values()), events=report)
        else:
            solution = solve_ivp(model,[self.start,self.stop],list(self.conditions.values()))
        return solution

def test_solver():
    s = Solver()
    s.addVar("theta")
    s.addVar("omega")
    s.equations["theta"] = "omega"
    s.equations["omega"] = "-0.25*omega - 5*sin(theta)"
    s.conditions["theta"] = 3
    s.conditions["omega"] = 0
    sol = s.solve()
    #sol = s.solve(progress_cb=print)
