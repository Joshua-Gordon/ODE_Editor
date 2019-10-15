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
        return 1
    
    def data(self, idx, role):
        if role == Qt.DisplayRole:
            row = idx.row()
            if 0 <= row < len(self.slv.equations):
                return QVariant(self.slv.equations[row])
        return QVariant()

    def headerData(self, section, orient, role):
        if orient == Qt.Vertical:
            if role == Qt.DisplayRole:
                return QVariant(f'Eq {section+1}')
        else:
            if section == 0 and role == Qt.DisplayRole:
                return QVariant('Equation')
        return QVariant()

class OEqnTable(QTableView):
    def __init__(self, slv):
        QTableView.__init__(self)

        self.model = OEqnModel(slv)
        self.setModel(self.model)

class OEqnEditor(QWidget):
    def __init__(self, slv):
        QWidget.__init__(self)
        self.slv = slv

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = OEqnTable(self.slv)
        self.layout.addWidget(self.table)

        self.varadd = QWidget(self)
        self.varfrm = QHBoxLayout()
        self.varadd.setLayout(self.varfrm)
        self.varname = QLineEdit(self)
        self.varfrm.addWidget(self.varname)
        self.varbut = QPushButton('Add', self)
        self.varfrm.addWidget(self.varbut)
        self.layout.addWidget(self.varadd)

class OMainWindow(QMainWindow):
    TITLE = 'ODE Editor'

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(self.TITLE)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        self.fmenu = self.menuBar().addMenu('File')
        self.fmenu.addAction('New', self.fnew)
        self.fmenu.addAction('Save', self.fsave)

    def fnew(self):
        slv = solver.Solver()
        slv.equations = ['a', 'b', 'c']
        widget = OEqnEditor(slv)
        self.tabs.addTab(widget, 'unnamed')

    def fsave(self):
        pass
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = OMainWindow()
    win.fnew()
    win.show()
    exit(app.exec_())
