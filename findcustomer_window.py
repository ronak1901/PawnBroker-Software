from PyQt5.QtWidgets import  QMainWindow, QWidget, QApplication, QLabel, QPushButton, QMdiArea, QMenuBar, QMenu ,QDateEdit, QTableWidget,QLineEdit, QTextEdit, QCompleter,QRadioButton, QComboBox, QTableWidgetItem, QAction, QMessageBox, QFileDialog,QListWidget
from PyQt5 import uic,QtCore,QtGui,QtWidgets
from PyQt5.QtGui import QFont,QTextDocument
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtPrintSupport import QPrinter,QPrintDialog,QPrintPreviewDialog
import sys
from datetime import date, datetime
import sqlite3
import fiscalyear
import pyautogui
from scaling import scaling



class Ui_FindCustWindow(QMainWindow):

    def __init__(self,x):
        global dbPath
        dbPath = x

        super(Ui_FindCustWindow, self).__init__()
        self.setupUi(self)


        listofwidgets = [self.name, self.city, self.phoneno, self.searchbutton, self.table, self.label, self.label_2, self.label_3]
        scaling(listofwidgets)

        self.searchbutton.clicked.connect(self.searchCustomerDetails)


    def searchCustomerDetails(self):
            global dbPath

            customerName = '%' + self.name.text() + '%'

            # print(customerName)
            customerCity = '%' + self.city.text() + '%'
            customerPhone = '%' + self.phoneno.text() + '%'
            # sqlQuery = 'select * from CustomerDetails where CustomerName LIKE "%i%"
            conn = sqlite3.connect(dbPath)
            c = conn.cursor()

            c.execute("SELECT * FROM CustomerDetails WHERE CustomerName LIKE ? AND City LIKE ? AND PhoneNo LIKE ? ",
                      [customerName, customerCity, customerPhone, ])
            # c.fetchall()
            customerList = c.fetchall()
            rownum = len(customerList)
            self.table.setRowCount(rownum)

            self.table.setColumnCount(11)

            self.table.setHorizontalHeaderLabels(('Name', 'Father Name', 'D.No', 'Street', 'City', 'PinCode',
                                                  'Phone No', 'Alternate', 'Other ', 'Ref Name', 'Date'))

            rowCount = 0

            for customers in customerList:
                    # self.table.setItem(rowCount, 0, QTableWidgetItem(str(rowCount+1)))
                    self.table.setItem(rowCount, 0, QTableWidgetItem(str(customers[0])))
                    self.table.setItem(rowCount, 1, QTableWidgetItem(str(customers[1])))
                    self.table.setItem(rowCount, 2, QTableWidgetItem(str(customers[2])))
                    self.table.setItem(rowCount, 3, QTableWidgetItem(str(customers[3])))
                    self.table.setItem(rowCount, 4, QTableWidgetItem(str(customers[4])))
                    self.table.setItem(rowCount, 5, QTableWidgetItem(str(customers[5])))
                    self.table.setItem(rowCount, 6, QTableWidgetItem(str(customers[6])))
                    self.table.setItem(rowCount, 7, QTableWidgetItem(str(customers[7])))
                    self.table.setItem(rowCount, 8, QTableWidgetItem(str(customers[8])))
                    self.table.setItem(rowCount, 9, QTableWidgetItem(str(customers[9])))
                    self.table.setItem(rowCount, 10, QTableWidgetItem(str(customers[10])))

                    rowCount += 1

            conn.commit()
            conn.close()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 820)
        MainWindow.setMinimumSize(QtCore.QSize(1240, 660))
        MainWindow.setStyleSheet("QMainWindow{\n"
"background: rgb(241, 250, 238);\n"
"}\n"
"\n"
"\n"
"QLineEdit{\n"
"\n"
"background: #a8dadc;\n"
"border: 2px solid rgb(29, 53, 87);\n"
"border-radius : 10px\n"
"\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"\n"
"border: 2px solid #e63946;\n"
"}\n"
"\n"
"\n"
"QTextEdit{\n"
"\n"
"background: #a8dadc;\n"
"border: 2px solid rgb(29, 53, 87);\n"
"border-radius : 15px\n"
"\n"
"}\n"
"\n"
"QTextEdit:focus{\n"
"\n"
"border: 2px solid #e63946;\n"
"}\n"
"\n"
"QLabel{\n"
"background-color:transparent;\n"
"}\n"
"\n"
"QPushButton{\n"
"    \n"
"    \n"
"    background-color: #1d3557;\n"
"    border-radius:8px;\n"
"    color: rgb(241, 250, 238);\n"
"    border : 4px solid #457b9d;\n"
"\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    \n"
"    background-color: rgb(241, 250, 238);\n"
"    border-radius:15px;\n"
"    border : 4px solid rgb(29, 53, 87);\n"
"    color: rgb(29, 53, 87);\n"
"    \n"
"\n"
"}\n"
"\n"
"QPushButton:clicked,\n"
"QPushButton:pressed{\n"
"\n"
"    \n"
"    \n"
"    background-color: rgb(230, 57, 70);\n"
"    border : 4px solid rgb(29, 53, 87);\n"
"    color: rgb(241, 250, 238);\n"
"    \n"
"\n"
"}\n"
"QDateEdit{\n"
"\n"
"background: #a8dadc;\n"
"border: 2px solid rgb(29, 53, 87);\n"
"\n"
"\n"
"}\n"
"\n"
"QDateEdit:focus{\n"
"\n"
"border: 2px solid #e63946;\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(280, 150, 121, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(280, 50, 81, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(280, 100, 81, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.city = QtWidgets.QLineEdit(self.centralwidget)
        self.city.setGeometry(QtCore.QRect(420, 100, 281, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.city.setFont(font)
        self.city.setObjectName("city")
        self.phoneno = QtWidgets.QLineEdit(self.centralwidget)
        self.phoneno.setGeometry(QtCore.QRect(420, 150, 191, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.phoneno.setFont(font)
        self.phoneno.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.phoneno.setMaxLength(10)
        self.phoneno.setObjectName("phoneno")
        self.name = QtWidgets.QLineEdit(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(420, 50, 591, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.name.setFont(font)
        self.name.setText("")
        self.name.setObjectName("name")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(50, 300, 1211, 451))
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.searchbutton = QtWidgets.QPushButton(self.centralwidget)
        self.searchbutton.setGeometry(QtCore.QRect(600, 210, 121, 51))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.searchbutton.setFont(font)
        self.searchbutton.setAutoDefault(True)
        self.searchbutton.setDefault(False)
        self.searchbutton.setObjectName("searchbutton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.name, self.city)
        MainWindow.setTabOrder(self.city, self.phoneno)
        MainWindow.setTabOrder(self.phoneno, self.searchbutton)
        MainWindow.setTabOrder(self.searchbutton, self.table)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Find Customer"))
        self.label_3.setText(_translate("MainWindow", "Phone No"))
        self.label.setText(_translate("MainWindow", "Name"))
        self.label_2.setText(_translate("MainWindow", "City"))
        self.searchbutton.setText(_translate("MainWindow", "Search"))


