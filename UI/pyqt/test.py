import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(476, 308)
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        #For rest of program to know which exercises to pick
        self.options ={'option 1':0, 'option 2':0, 'option 3':0, 'option 4':0}

        # For showing message
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, 80, 191, 20))

        self.checkBox_1 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_1.setGeometry(QtCore.QRect(170, 120, 81, 20))
        self.checkBox_1.stateChanged.connect(self.checked1)

        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(170, 140, 81, 20))
        self.checkBox_2.stateChanged.connect(self.checked2)

        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(170, 160, 81, 20))
        self.checkBox_3.stateChanged.connect(self.checked3)

        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setGeometry(QtCore.QRect(170, 180, 81, 20))
        self.checkBox_4.stateChanged.connect(self.checked4)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def checked1(self, checked):
        self.options['option 1'] = checked

    def checked2(self, checked):
        self.options['option 2'] = checked

    def checked3(self, checked):
        self.options['option 3'] = checked

    def checked4(self, checked):
        self.options['option 4'] = checked

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.label.setText(_translate("MainWindow", "Select your preferred exercises"))
        self.checkBox_1.setText(_translate("MainWindow", "Option 1"))
        self.checkBox_2.setText(_translate("MainWindow", "Option 2"))
        self.checkBox_3.setText(_translate("MainWindow", "Option 3"))
        self.checkBox_4.setText(_translate("MainWindow", "Option 4"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
