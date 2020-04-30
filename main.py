import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import solver

class OEqnModel(QAbstractTableModel):
    def __init__(self, slv):
        QAbstractTableModel.__init__(self)
        self.slv = slv

    def rowCount(self, parent):
        return len(self.slv.equations)

    def columnCount(self, parent):
        return 2

    def data(self, idx, role):
        if role in (Qt.DisplayRole, Qt.EditRole):
            row = idx.row()
            col = idx.column()
            sel = (self.slv.equations, self.slv.conditions)[col]
            if 0 <= row < len(sel):
                return QVariant(sel[list(sel.keys())[row]])
        return QVariant()

    def flags(self, idx):
        return QAbstractTableModel.flags(self, idx) | Qt.ItemIsEditable

    def setData(self, idx, value, role):
        if role == Qt.EditRole:
            row = idx.row()
            col = idx.column()
            sel = (self.slv.equations, self.slv.conditions)[col]
            conv = lambda x: x
            if col == 1:
                conv = float
            if 0 <= row < len(sel):
                try:
                    sel[list(sel.keys())[row]] = conv(value)
                except ValueError:
                    return False
                return True
        return False

    COLUMNS = ['Equation', 'Initial']

    def headerData(self, section, orient, role):
        if orient == Qt.Vertical:
            if role == Qt.DisplayRole and 0 <= section < len(self.slv.equations):
                return QVariant(list(self.slv.equations.keys())[section] + "' =")
        else:
            if role == Qt.DisplayRole:
                return QVariant(self.COLUMNS[section])
        return QVariant()

    def addVar(self, var):
        if var in self.slv.equations:
            return False
        row = len(self.slv.equations)
        self.beginInsertRows(QModelIndex(), row, row)
        self.slv.addVar(var)
        self.endInsertRows()

class OEqnTable(QTableView):
    def __init__(self, slv):
        QTableView.__init__(self)

        self.mdl = OEqnModel(slv)
        self.setModel(self.mdl)

class OEqnEditor(QWidget):
    def __init__(self, slv, tabs):
        QWidget.__init__(self)
        self.slv = slv
        self.tabs = tabs

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = OEqnTable(self.slv)
        self.layout.addWidget(self.table)

        self.varadd = QWidget(self)
        self.varfrm = QHBoxLayout()
        self.varadd.setLayout(self.varfrm)
        self.varname = QLineEdit(self)
        self.varname.returnPressed.connect(self.vadd)
        self.varfrm.addWidget(self.varname)
        self.varbut = QPushButton('Add', self)
        self.varbut.clicked.connect(self.vadd)
        self.varfrm.addWidget(self.varbut)
        self.varrun = QPushButton('Run', self)
        self.varrun.clicked.connect(self.vrun)
        self.varfrm.addWidget(self.varrun)
        self.layout.addWidget(self.varadd)

    def vadd(self):
        name = self.varname.text()
        if not name:
            return
        mdl = self.table.model().addVar(name)

    def vrun(self):
        graph = OGraph(self.slv.equations.keys())
        view = QGraphicsView(graph)
        self.tabs.addTab(view, "render")
        #view = OGraphView(graph)
        #view.show()
        def cb(t, Y):
            print(t, Y)
            for idx, y in enumerate(Y):
                graph.addPoint(idx, t, y)
        self.slv.solve(cb)
        view.fitInView(graph.itemsBoundingRect())

class OGraph(QGraphicsScene):
    def __init__(self, series):
        QGraphicsScene.__init__(self)

        series = list(series)

        self.series = series
        self.paths = [QPainterPath() for _ in series]
        self.init = [True for _ in series]
        self.pen = QPen()
        self.pen.setCosmetic(True)
        self.items = [self.addPath(p, self.pen) for p in self.paths]

    def addPoint(self, ser, x, y):
        if self.init[ser]:
            self.paths[ser].moveTo(x, y)
            self.init[ser] = False
        else:
            self.paths[ser].lineTo(x, y)
            self.items[ser].setPath(self.paths[ser])
            #self.changed.emit([self.paths[ser].boundingRect()])

class OGraphView(QDialog):
    def __init__(self, graph):
        QDialog.__init__(self)

        self.view = QGraphicsView(graph, self)

class OMainWindow(QMainWindow):
    TITLE = 'ODE Editor'

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(self.TITLE)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tclose)
        self.setCentralWidget(self.tabs)

        self.fmenu = self.menuBar().addMenu('File')
        self.fmenu.addAction('New', self.fnew)
        self.fmenu.addAction('Open', self.fopen)
        self.fmenu.addAction('Save', self.fsave)

    def tclose(self, idx):
        self.tabs.widget(idx).close()
        self.tabs.removeTab(idx)

    def fnew(self):
        slv = solver.Solver()
        widget = OEqnEditor(slv, self.tabs)
        self.tabs.addTab(widget, 'unnamed')

    def fsave(self):
        pass

    def fopen(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = OMainWindow()
    win.fnew()
    win.show()
    exit(app.exec_())

#run with python3 only
