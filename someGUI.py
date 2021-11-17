import sys
from PyQt5 import QtWidgets  # , QtGui, QtCore
from randomNameGen import main as getRandomTitle

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUI()

    def setupUI(self):
        self.resize(220, 120)
        self.displayLabel = QtWidgets.QLabel(self)
        self.displayLabel.setGeometry(10,10,200,30)
        
        self.button = QtWidgets.QPushButton(self)
        self.button.setText("generate project name")
        self.button.setGeometry(10,50,200,50)

        self.button.pressed.connect(self.displayRandomTitle)

    def displayRandomTitle(self):
        self.displayLabel.setText(getRandomTitle())


def main():

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
