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



class Ui_Form(QWidget):

    def __init__(self,x):
        global dbPath
        dbPath = x


        super(Ui_Form, self).__init__()
        self.setupUi(self)

        listofwidgets = [self.createbutton, self.nameofdb]
        scaling(listofwidgets)

        self.createbutton.clicked.connect(self.create_db)




    def create_db(self):
        global dbPath


        if (self.nameofdb.text() == ''):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Enter a Database Name !!")
            msg.exec_()


        else:
            global dbPath
            newdbPath = "D:\Software\\" + self.nameofdb.text() + ".db"
            conn = sqlite3.connect(newdbPath)
            c = conn.cursor()

            c.execute("""CREATE TABLE IF NOT EXISTS CustomerDetails(
    						CustomerName	TEXT NOT NULL ,
    						FatherName	TEXT NOT NULL,
    						DoorNo TEXT,
    						Street	TEXT,
    						City	TEXT NOT NULL,
    						Pincode	TEXT,
    						PhoneNo TEXT,
    						PhNo	TEXT,
    						OtherDetails	TEXT,
    						ReferenceName	TEXT,
    						Date	TEXT NOT NULL
    						)""")

            c.execute("""CREATE TABLE IF NOT EXISTS PledgeDetails(
    							CustomerId TEXT NOT NULL,
    							PledgeNum TEXT NOT NULL ,
    							PledgeDate TEXT NOT NULL,
    							ArticleType TEXT NOT NULL,
    							AD1 TEXT NOT NULL,
    							AD2 TEXT,
    							AD3 TEXT,
    							GWt TEXT NOT NULL,
    							NWt TEXT NOT NULL,
    							NOP TEXT NOT NULL,
    							Purity TEXT NOT NULL,
    							Amount TEXT NOT NULL,
    							RateOfInterest TEXT NOT NULL,
    							AdvanceInterest TEXT,
    							Status TEXT NOT NULL,
    							InterestCollected TEXT,
    							ReleaseDate TEXT,
    							FinancialYear TEXT NOT NULL

    						)""")

            # print(dbPath)
            c.execute("ATTACH DATABASE '%s' as oldDb" % dbPath)
            c.execute("INSERT INTO CustomerDetails SELECT * FROM oldDb.CustomerDetails")
            c.execute("INSERT INTO PledgeDetails SELECT * FROM oldDb.pledgeDetails where status = 1")

            # print(self)
            # self.createbutton.setEnabled(False)
            self.parent().close()

            conn.commit()
            conn.close()




            dbPath = newdbPath





    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(372, 233)
        Form.setMinimumSize(QtCore.QSize(372, 233))
        Form.setStyleSheet("QMainWindow{\n"
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
        self.nameofdb = QtWidgets.QLineEdit(Form)
        self.nameofdb.setGeometry(QtCore.QRect(60, 70, 251, 41))
        self.nameofdb.setClearButtonEnabled(True)
        self.nameofdb.setObjectName("nameofdb")
        self.createbutton = QtWidgets.QPushButton(Form)
        self.createbutton.setGeometry(QtCore.QRect(140, 150, 91, 41))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.createbutton.setFont(font)
        self.createbutton.setStyleSheet("")
        self.createbutton.setAutoDefault(True)
        self.createbutton.setDefault(True)
        self.createbutton.setObjectName("createbutton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Create New Financial Year"))
        self.nameofdb.setPlaceholderText(_translate("Form", "Enter here"))
        self.createbutton.setText(_translate("Form", "DONE"))


