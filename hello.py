import sys
#from PyQt5 import QtWidgets
from Qt import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    button = QtWidgets.QPushButton("Hello World")
    button.show()
    sys.exit(app.exec_())
