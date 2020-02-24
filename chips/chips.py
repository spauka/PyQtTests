import sys
from Qt import QtCore, QtGui, QtWidgets

from chip import Chip

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_DontCreateNativeWidgetSiblings)

    window = QtWidgets.QWidget()
    scene = QtWidgets.QGraphicsScene(window)
    chip = Chip(QtGui.QColor(QtCore.Qt.green), 0, 0)
    scene.addItem(chip)

    layout = QtWidgets.QGridLayout()
    view = QtWidgets.QGraphicsView(scene)
    layout.addWidget(view)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec_())
