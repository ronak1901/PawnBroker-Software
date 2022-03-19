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




class Ui_CutstomerWindow(QMainWindow):


    def __init__(self,x):
        global dbPath
        dbPath = x

        super(Ui_CutstomerWindow, self).__init__()
        self.setupUi(self)

        listofwidgets = [self.name, self.fname, self.doorno, self.street, self.city, self.pincode, self.phoneno,self.altno, self.otherdet, self.refname,
                         self.label,self.label_2, self.label_3, self.label_4, self.label_5, self.label_6, self.label_7, self.label_8,
                         self.label_9, self.label_10, self.label_11, self.savebutton, self.dt]
        scaling(listofwidgets)

        self.dt.setDate(date.today())
        conn = sqlite3.connect(dbPath)

        c = conn.cursor()
        c.execute("SELECT CustomerName FROM CustomerDetails")


        items = c.fetchall()
        customernames = []
        for item in items:
                customernames.append(item[0])


        c.execute("SELECT City FROM CustomerDetails")
        items = c.fetchall()
        city = []

        for item in items:
                if(item[0] not in city):
                        city.append(item[0])


        c.execute("SELECT Street FROM CustomerDetails")
        items = c.fetchall()
        streets = []

        for item in items:
                if (item[0] not in streets):
                        streets.append(item[0])


        conn.commit()
        conn.close()

        self.completer = QCompleter(customernames)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.name.setCompleter(self.completer)

        self.completer2 = QCompleter(city)
        self.completer2.setCaseSensitivity(Qt.CaseInsensitive)
        self.city.setCompleter(self.completer2)

        self.completer3 = QCompleter(streets)
        self.completer3.setCaseSensitivity(Qt.CaseInsensitive)
        self.street.setCompleter(self.completer3)

        # self.savebutton.clicked.connect(lambda: self.save_data(customernames))
        # self.name.returnPressed.connect(lambda: self.checkName(customernames))

        # self.savebutton.clicked.connect(self.edit_data)
        # self.name.returnPressed.connect(self.fill_data)



    def checkName(self):
        global dbPath


        conn = sqlite3.connect(dbPath)
        c = conn.cursor()
        c.execute("SELECT CustomerName FROM CustomerDetails")
        items = c.fetchall()
        customernames = []

        for item in items:
                customernames.append(item[0])

        conn.commit()
        conn.close()

        if (self.name.text() in customernames):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Name alerady Exists !!")
                msg.exec_()


    def save_data(self):
            global dbPath

            conn = sqlite3.connect(dbPath)

            c = conn.cursor()

            c.execute("SELECT CustomerName FROM CustomerDetails")

            items = c.fetchall()
            customernames = []
            for item in items:
                    customernames.append(item[0])

            # inserting data into database
            data_to_insert = [self.name.text(), self.fname.text(), self.doorno.text(), self.street.text(),
                              self.city.text(),
                              self.pincode.text(), self.phoneno.text(), self.altno.text(), self.otherdet.text(),
                              self.refname.text(), self.dt.text()]
            dataItems = [self.name.text(), self.fname.text(), self.city.text()]

            msg = QMessageBox()
            # print("inside if")

            msg.setIcon(QMessageBox.Warning)
            if (len(dataItems[0]) == 0):
                    msg.setText("Please Enter a Name")
                    msg.exec_()
            elif (len(dataItems[1]) == 0):
                    msg.setText("Please Enter Husband/Father Name")
                    msg.exec_()
            elif (len(dataItems[2]) == 0):
                    msg.setText("Please Enter The City")
                    msg.exec_()
            elif (self.name.text() in customernames):
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Name alerady Exists !!")
                    msg.exec_()

            else:

                    c.execute("INSERT INTO CustomerDetails VALUES (?,?,?,?,?,?,?,?,?,?,?)", data_to_insert)
                    self.name.setText("")
                    self.fname.setText("")
                    self.doorno.setText("")
                    self.street.setText("")
                    self.city.setText("")
                    self.pincode.setText("")
                    self.phoneno.setText("")
                    self.altno.setText("")
                    self.otherdet.setText("")
                    self.refname.setText("")
            # print(self.name.text())

            conn.commit()

            conn.close()



    def fill_data(self):
            global dbPath

            global cust_id

            conn = sqlite3.connect(dbPath)
            c = conn.cursor()

            c.execute("SELECT CustomerName FROM CustomerDetails")

            items = c.fetchall()
            customernames = []
            for item in items:
                    customernames.append(item[0])

            c.execute("SELECT rowid FROM CustomerDetails WHERE CustomerName = (?)", [self.name.text()])
            customer_id = c.fetchall()[0]
            cust_id = customer_id[0]

            if (self.name.text() in customernames):
                    c.execute(
                            "SELECT FatherName, DoorNo, Street, City, Pincode, PhoneNo, PhNO, OtherDetails, ReferenceName FROM CustomerDetails WHERE CustomerName = (?)",
                            [self.name.text()])
                    x = c.fetchall()
                    info = list(x[0])

                    self.fname.setText(info[0])
                    self.doorno.setText(info[1])
                    self.street.setText(info[2])
                    self.city.setText(info[3])
                    self.pincode.setText(info[4])
                    self.phoneno.setText(info[5])
                    self.altno.setText(info[6])
                    self.otherdet.setText(info[7])
                    self.refname.setText(info[8])

            else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Name doesnot Exist !!")
                    msg.exec_()

            conn.commit()
            conn.close()



    def edit_data(self):
            global cust_id
            global dbPath

            conn = sqlite3.connect(dbPath)
            c = conn.cursor()
            # c.execute("SELECT rowid FROM CustomerDetails WHERE CustomerName = (?)", [self.name.text()])
            # customer_id = c.fetchall()[0]

            if (len(self.name.text()) == 0):

                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Please Enter a Name")
                    msg.exec_()


            else:
                    data_to_insert = [self.name.text(), self.fname.text(), self.doorno.text(), self.street.text(),self.city.text(), self.pincode.text(), self.phoneno.text(),
                                      self.altno.text(), self.otherdet.text(),self.refname.text(), cust_id]

                    c.execute(
                            "UPDATE CustomerDetails SET CustomerName = ?, FatherName = ?, DoorNo = ?, Street = ?, City = ?, Pincode = ?, PhoneNo = ?,"
                            " PhNo = ?, OtherDetails = ?, ReferenceName = ? WHERE rowid = ?", data_to_insert)
                    self.parent().close()

            conn.commit()
            conn.close()




    def setupUi(self, CutstomerWindow):
        CutstomerWindow.setObjectName("CutstomerWindow")
        CutstomerWindow.resize(1330, 810)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CutstomerWindow.sizePolicy().hasHeightForWidth())
        CutstomerWindow.setSizePolicy(sizePolicy)
        CutstomerWindow.setMinimumSize(QtCore.QSize(0, 0))
        CutstomerWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        CutstomerWindow.setAcceptDrops(False)
        CutstomerWindow.setStyleSheet("QMainWindow{\n"
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
"    border-radius:15px;\n"
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
        self.centralwidget = QtWidgets.QWidget(CutstomerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 120, 81, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 350, 81, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(110, 280, 101, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(680, 280, 81, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(110, 420, 141, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(680, 350, 111, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(680, 420, 141, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(110, 490, 171, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(110, 560, 191, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(110, 180, 101, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.name = QtWidgets.QLineEdit(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(300, 120, 591, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.fname = QtWidgets.QLineEdit(self.centralwidget)
        self.fname.setGeometry(QtCore.QRect(300, 210, 541, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.fname.setFont(font)
        self.fname.setObjectName("fname")
        self.doorno = QtWidgets.QLineEdit(self.centralwidget)
        self.doorno.setGeometry(QtCore.QRect(300, 280, 181, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.doorno.setFont(font)
        self.doorno.setObjectName("doorno")
        self.street = QtWidgets.QLineEdit(self.centralwidget)
        self.street.setGeometry(QtCore.QRect(830, 280, 451, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.street.setFont(font)
        self.street.setObjectName("street")
        self.city = QtWidgets.QLineEdit(self.centralwidget)
        self.city.setGeometry(QtCore.QRect(300, 350, 281, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.city.setFont(font)
        self.city.setObjectName("city")
        self.pincode = QtWidgets.QLineEdit(self.centralwidget)
        self.pincode.setGeometry(QtCore.QRect(830, 350, 141, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.pincode.setFont(font)
        self.pincode.setObjectName("pincode")
        self.phoneno = QtWidgets.QLineEdit(self.centralwidget)
        self.phoneno.setGeometry(QtCore.QRect(300, 420, 191, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.phoneno.setFont(font)
        self.phoneno.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.phoneno.setMaxLength(10)
        self.phoneno.setObjectName("phoneno")
        self.altno = QtWidgets.QLineEdit(self.centralwidget)
        self.altno.setGeometry(QtCore.QRect(830, 420, 201, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.altno.setFont(font)
        self.altno.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.altno.setMaxLength(10)
        self.altno.setClearButtonEnabled(False)
        self.altno.setObjectName("altno")
        self.otherdet = QtWidgets.QLineEdit(self.centralwidget)
        self.otherdet.setGeometry(QtCore.QRect(300, 490, 721, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.otherdet.setFont(font)
        self.otherdet.setObjectName("otherdet")
        self.refname = QtWidgets.QLineEdit(self.centralwidget)
        self.refname.setGeometry(QtCore.QRect(300, 560, 431, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.refname.setFont(font)
        self.refname.setObjectName("refname")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(110, 210, 181, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.savebutton = QtWidgets.QPushButton(self.centralwidget)
        self.savebutton.setGeometry(QtCore.QRect(620, 640, 111, 51))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.savebutton.setFont(font)
        self.savebutton.setAutoDefault(True)
        self.savebutton.setDefault(True)
        self.savebutton.setObjectName("savebutton")
        self.dt = QtWidgets.QDateEdit(self.centralwidget)
        self.dt.setEnabled(True)
        self.dt.setGeometry(QtCore.QRect(1090, 110, 121, 41))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        self.dt.setFont(font)
        self.dt.setAutoFillBackground(False)
        self.dt.setReadOnly(True)
        self.dt.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dt.setKeyboardTracking(True)
        self.dt.setProperty("showGroupSeparator", False)
        self.dt.setTimeSpec(QtCore.Qt.LocalTime)
        self.dt.setObjectName("dt")
        CutstomerWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CutstomerWindow)
        QtCore.QMetaObject.connectSlotsByName(CutstomerWindow)

    def retranslateUi(self, CutstomerWindow):
        _translate = QtCore.QCoreApplication.translate
        CutstomerWindow.setWindowTitle(_translate("CutstomerWindow", "New Customer"))
        self.label.setText(_translate("CutstomerWindow", "Name"))
        self.label_2.setText(_translate("CutstomerWindow", "City"))
        self.label_3.setText(_translate("CutstomerWindow", "Door No"))
        self.label_4.setText(_translate("CutstomerWindow", "Street"))
        self.label_5.setText(_translate("CutstomerWindow", "Phone No"))
        self.label_6.setText(_translate("CutstomerWindow", "Pin Code"))
        self.label_7.setText(_translate("CutstomerWindow", "Alternate No"))
        self.label_8.setText(_translate("CutstomerWindow", "Other Details"))
        self.label_9.setText(_translate("CutstomerWindow", "Reference Name"))
        self.label_10.setText(_translate("CutstomerWindow", "Father /"))
        self.label_11.setText(_translate("CutstomerWindow", "Husband\'s name"))
        self.savebutton.setText(_translate("CutstomerWindow", "save"))



