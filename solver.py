import collections
from scipy.integrate import solve_ivp
from numpy import *

import json

class Solver(object):
    def __init__(self):
        self.equations = collections.OrderedDict()
        self.conditions = collections.OrderedDict()
        self.start = 0
        self.stop = 1

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
                progress_cb(t, Y)
                return True
            solution = solve_ivp(model,[self.start,self.stop],list(self.conditions.values()), events=report)
        else:
            solution = solve_ivp(model,[self.start,self.stop],list(self.conditions.values()))
        return solution

    def toJSON(self):
        return json.dumps(vars(self))

    def fromJSON(self,txt):
        js = json.loads(txt)
        self.equations = collections.OrderedDict(js["equations"])
        self.conditions = collections.OrderedDict(js["conditions"])
        self.start = float(js["start"])
        self.stop = float(js["stop"])

    def __repr__(self):
        return f'<Solver eq={self.equations!r} co={self.conditions!r}>'

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
    print(s.toJSON())
    j = s.toJSON()
    t = Solver()
    t.fromJSON(j)
    print(t.solve())
    print(s.solve())
