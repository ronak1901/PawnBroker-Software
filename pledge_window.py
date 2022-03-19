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



class Ui_Pledge_Windoow(QMainWindow):

    def __init__(self,x):
        global dbPath
        dbPath = x


        super(Ui_Pledge_Windoow, self).__init__()
        self.setupUi(self)

        listofwidgets = [self.pledgeno, self.searchbar, self.address, self.ad1, self.ad2, self.ad3, self.gwt, self.nwt, self.nop, self.purity, self.principal,
                         self.interest,self.intmonth, self.intcollected, self.goldradio, self.silverradio, self.savebutton, self.pledgedate,
                         self.label, self.label_2, self.label_3, self.label_4,self.label_5, self.label_6, self.label_7, self.label_8, self.label_9, self.label_10, self.label_11,
                         self.label_12, self.label_13, self.label_14]
        scaling(listofwidgets)



        self.pledgedate.setDate(date.today())
        # self.pledgedate.setMaximumDate(date.today())

        conn = sqlite3.connect(dbPath)

        c = conn.cursor()
        c.execute("SELECT CustomerName FROM CustomerDetails")

        items = c.fetchall()
        customernames = []
        for item in items:
                customernames.append(item[0])

        conn.commit()
        conn.close()

        self.completer = QCompleter(customernames)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)

        # self.searchbar.returnPressed.connect(onPressed)

        # get customer details on entering name
        def onPressed():
                if (self.searchbar.text() in customernames):
                        conn = sqlite3.connect(dbPath)
                        c = conn.cursor()
                        # print("key event")
                        c.execute(
                                "SELECT FatherName, DoorNo, Street, City, Pincode, PhoneNo FROM CustomerDetails WHERE CustomerName = (?)",
                                [self.searchbar.text()])
                        x = c.fetchall()
                        addr = list(x[0])
                        # print(addr)
                        self.address.setText(
                                f"Father/Husband : {addr[0]} \n{addr[1]}, {addr[2]}, \n{addr[3]}, {addr[4]},\nPhoneNo : {addr[5]} ")
                        conn.commit()
                        conn.close()

                        if self.goldradio.isChecked():
                                self.purity.setText("75%")

                        else:
                                self.purity.setText("60%")


                else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText("Please Select the name from the list")
                        msg.exec_()

        self.searchbar.returnPressed.connect(onPressed)

        # display interest per month

        def onpress():
                p = float(self.principal.text())

                if (len(self.interest.text()) == 0):
                        r = 0
                else:
                        r = float(self.interest.text())
                icm = p * r / 100

                self.intmonth.setText(str(icm))

        self.interest.returnPressed.connect(onpress)

        # self.savebutton.clicked.connect(self.savepledge)




    def savepledge(self):

            global dbPath
            # radio button
            self.loantype = ""


            if self.goldradio.isChecked():
                    self.loantype = "gold"
            else:
                    self.loantype = "silver"

            conn = sqlite3.connect(dbPath)
            c = conn.cursor()

            dateString = self.pledgedate.text()
            dates = dateString.split("-")
            # print(dates)
            fiscalyear.START_MONTH = 4
            fYear = (fiscalyear.FiscalDate(int(dates[2]), int(dates[1]), int(dates[0]))).fiscal_year

            c.execute("select PledgeNum from PledgeDetails where FinancialYear = ?", [fYear])
            listNum = c.fetchall()
            pledgeNumberList = []
            for num in listNum:
                    pledgeNumberList.append(num[0])
            # print(pledgeNumberList)

            if (self.pledgeno.text() in pledgeNumberList):
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Pledge Number Already EXISTS !!")
                    msg.exec_()
            else:

                    if (len(self.searchbar.text()) == 0):
                            msg = QMessageBox()
                            msg.setIcon(QMessageBox.Warning)
                            msg.setText("Please Enter the Name")
                            msg.exec_()

                    else:
                            c.execute("SELECT rowid FROM CustomerDetails WHERE CustomerName = (?)",
                                      [self.searchbar.text()])
                            customer_id = c.fetchall()[0]
                            pledgedata = [customer_id[0], self.pledgeno.text(), self.pledgedate.text(), self.loantype,
                                          self.ad1.text(), self.ad2.text(), self.ad3.text(),
                                          self.gwt.text(), self.nwt.text(), self.nop.text(), self.purity.text(),
                                          self.principal.text(), self.interest.text(), self.intcollected.text(), "1",
                                          "", "", fYear]

                            pledgedataitem = [self.pledgeno.text(), self.gwt.text(), self.nop.text(),
                                              self.principal.text(),
                                              self.interest.text(), self.intcollected.text()]

                            if (len(pledgedataitem[0]) == 0 or len(pledgedataitem[1]) == 0 or len(
                                    pledgedataitem[2]) == 0 or len(pledgedataitem[3]) == 0 ):#or len(pledgedataitem[4]) == 0 or len(pledgedataitem[5]) == 0

                                    msg = QMessageBox()
                                    msg.setIcon(QMessageBox.Warning)
                                    msg.setText("Please Enter all the Required Details")
                                    msg.exec_()

                            else:
                                    c.execute("INSERT INTO PledgeDetails VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", pledgedata)
                                    self.pledgeno.setText("")
                                    self.searchbar.setText("")
                                    self.address.setText("")
                                    self.ad1.setText("")
                                    self.ad2.setText("")
                                    self.ad3.setText("")
                                    self.gwt.setText("")
                                    self.nwt.setText("")
                                    self.nop.setText("")
                                    self.purity.setText("")
                                    self.principal.setText("")
                                    self.interest.setText("")
                                    self.intcollected.setText("")
                                    self.intmonth.setText("")
                                    self.pledgedate.setDate(date.today())

            conn.commit()

            conn.close()



    def showpledgedata(self):
            global pledgeRowID
            global dbPath

            conn = sqlite3.connect(dbPath)
            c = conn.cursor()

            # c.execute("SELECT PledgeNum FROM PledgeDetails")
            # x = c.fetchall()[0]
            # if(self.pledgeno.text() in x):
            c.execute("SELECT PledgeNum FROM PledgeDetails")
            pleList = c.fetchall()
            pledgeList = []
            for pledgenum in pleList:
                    pledgeList.append(pledgenum[0])



            num = self.pledgeno.text()
            customerName = '%' + self.searchbar.text() + '%'

            # print(pledgeList)
            if (num in pledgeList):

                    c.execute(
                            "SELECT CustomerId,PledgeDate, ArticleType, AD1, AD2, AD3, GWt, NWt, NOP, Purity, Amount, RateOfInterest, AdvanceInterest, rowid ,Status FROM PledgeDetails WHERE PledgeNum = ?",
                            [self.pledgeno.text()])
                    pditem = c.fetchall()[0]
                    pledgeRowID = pditem[13]
                    # print(pditem[14])
                    if (pditem[14] == "0"):
                            # print("inside if")
                            msg = QMessageBox()
                            msg.setIcon(QMessageBox.Warning)
                            msg.setText("Pledge Already released")
                            msg.exec_()
                            self.parent().close()
                    else:

                            c.execute("SELECT CustomerName FROM CustomerDetails WHERE rowid = ?", (pditem[0]))
                            custm = c.fetchall()[0]

                            self.searchbar.setText(custm[0])
                            self.pledgedate.setDate(QtCore.QDate.fromString(pditem[1], "dd-MM-yyyy"))

                            if (pditem[2] == "gold"):
                                    self.goldradio.setChecked(True)

                            if (pditem[2] == "silver"):
                                    self.silverradio.setChecked(True)

                            self.ad1.setText(pditem[3])
                            self.ad2.setText(pditem[4])
                            self.ad3.setText(pditem[5])
                            self.gwt.setText(pditem[6])
                            self.nwt.setText(pditem[7])
                            self.nop.setText(pditem[8])
                            self.purity.setText(pditem[9])
                            self.principal.setText(pditem[10])
                            self.interest.setText(pditem[11])
                            self.intcollected.setText(pditem[12])

                    # else:
                    # msg = QMessageBox()
                    # msg.setIcon(QMessageBox.Warning)
                    # msg.setText("Pledge Does Not Exist !!")
                    # msg.exec_()
            else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Pledge DONOT Exists")
                    msg.exec_()
                    self.parent().close()

            conn.commit()
            conn.close()



    def pledgeEdit(self):
            global dbPath
            conn = sqlite3.connect(dbPath)
            c = conn.cursor()

            # c.execute("SELECT rowid FROM pledgedetails WHERE PledgeNum = ?", (self.pledgeno.text()))
            # pledgeRowID = c.fetchall()[0]
            # pledgeid = pledgeRowID[0]
            c.execute("SELECT rowid FROM CustomerDetails WHERE CustomerName = ?", [self.searchbar.text()])
            custRowID = c.fetchall()[0]
            if (self.goldradio.isChecked()):
                    articleType = "gold"
            else:
                    articleType = "silver"

            dateString = self.pledgedate.text()
            dates = dateString.split("-")
            # print(dates)
            fiscalyear.START_MONTH = 4
            fYear = (fiscalyear.FiscalDate(int(dates[2]), int(dates[1]), int(dates[0]))).fiscal_year

            c.execute("select PledgeNum from PledgeDetails where FinancialYear = ?", [fYear])
            listNum = c.fetchall()
            pledgeNumberList = []
            for num in listNum:
                    pledgeNumberList.append(num[0])
            # print(pledgeNumberList)

            # if (self.pledgeno.text() in pledgeNumberList):
            #         msg = QMessageBox()
            #         msg.setIcon(QMessageBox.Warning)
            #         msg.setText("Pledge Number Already EXISTS !!")
            #         msg.exec_()


            data_to_edit = [custRowID[0], self.pledgeno.text(), self.pledgedate.text(), articleType,
                            self.ad1.text(), self.ad2.text(), self.ad3.text(),
                            self.gwt.text(), self.nwt.text(), self.nop.text(), self.purity.text(),
                            self.principal.text(), self.interest.text(), self.intcollected.text(), fYear,
                            pledgeRowID ]

            c.execute(
                    "UPDATE PledgeDetails SET CustomerId = ?, PledgeNum = ?,PledgeDate=?, ArticleType = ?, AD1 = ?, AD2 = ?, AD3 = ?, GWt = ?, NWt = ?, NOP = ?, Purity = ?, Amount = ?, RateOfInterest = ?, AdvanceInterest = ? , FinancialYear = ?"
                    "WHERE rowid = ?", data_to_edit )


            self.parent().close()


            conn.commit()
            conn.close()




    def setupUi(self, Pledge_Windoow):
        Pledge_Windoow.setObjectName("Pledge_Windoow")
        Pledge_Windoow.setEnabled(True)
        Pledge_Windoow.resize(1330, 810)
        Pledge_Windoow.setMinimumSize(QtCore.QSize(0, 0))
        Pledge_Windoow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Pledge_Windoow.setStyleSheet("QMainWindow{\n"
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
"}")
        self.centralwidget = QtWidgets.QWidget(Pledge_Windoow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 110, 71, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color:transparent;")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(500, 60, 51, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color:transparent;")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(200, 350, 201, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color:transparent;")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(200, 300, 121, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color:transparent;")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(490, 500, 81, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color:transparent;")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(200, 500, 121, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background-color:transparent;")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(200, 160, 101, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("background-color:transparent;")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(200, 60, 121, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("background-color:transparent;")
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(750, 500, 71, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("background-color:transparent;")
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(990, 500, 81, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("background-color:transparent;")
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(200, 560, 101, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("background-color:transparent;")
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(200, 620, 101, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("background-color:transparent;")
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(200, 670, 191, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("background-color:transparent;")
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(510, 620, 151, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("background-color:transparent;")
        self.label_14.setObjectName("label_14")
        self.pledgeno = QtWidgets.QLineEdit(self.centralwidget)
        self.pledgeno.setGeometry(QtCore.QRect(330, 60, 113, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.pledgeno.setFont(font)
        self.pledgeno.setStyleSheet("\n"
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
"}")
        self.pledgeno.setObjectName("pledgeno")
        self.pledgedate = QtWidgets.QDateEdit(self.centralwidget)
        self.pledgedate.setGeometry(QtCore.QRect(570, 60, 151, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.pledgedate.setFont(font)
        self.pledgedate.setStyleSheet("\n"
"QDateEdit{\n"
"\n"
"background: #a8dadc;\n"
"border: 2px solid rgb(29, 53, 87);\n"
"border-radius: 5px\n"
"}\n"
"\n"
"QDateEdit:focus{\n"
"\n"
"border: 2px solid #e63946;\n"
"}")
        self.pledgedate.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.pledgedate.setObjectName("pledgedate")
        self.searchbar = QtWidgets.QLineEdit(self.centralwidget)
        self.searchbar.setGeometry(QtCore.QRect(330, 110, 731, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.searchbar.setFont(font)
        self.searchbar.setStyleSheet("\n"
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
"}")
        self.searchbar.setObjectName("searchbar")
        self.address = QtWidgets.QTextEdit(self.centralwidget)
        self.address.setEnabled(True)
        self.address.setGeometry(QtCore.QRect(330, 160, 771, 131))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.address.setFont(font)
        self.address.setStyleSheet("QTextEdit{\n"
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
"}")
        self.address.setReadOnly(True)
        self.address.setObjectName("address")
        self.silverradio = QtWidgets.QRadioButton(self.centralwidget)
        self.silverradio.setGeometry(QtCore.QRect(450, 300, 95, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.silverradio.setFont(font)
        self.silverradio.setStyleSheet("background-color:transparent;")
        self.silverradio.setObjectName("silverradio")
        self.goldradio = QtWidgets.QRadioButton(self.centralwidget)
        self.goldradio.setGeometry(QtCore.QRect(350, 300, 81, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.goldradio.setFont(font)
        self.goldradio.setStyleSheet("background-color:transparent;")
        self.goldradio.setChecked(True)
        self.goldradio.setObjectName("goldradio")
        self.ad1 = QtWidgets.QLineEdit(self.centralwidget)
        self.ad1.setGeometry(QtCore.QRect(430, 360, 641, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.ad1.setFont(font)
        self.ad1.setStyleSheet("\n"
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
"}")
        self.ad1.setObjectName("ad1")
        self.ad2 = QtWidgets.QLineEdit(self.centralwidget)
        self.ad2.setGeometry(QtCore.QRect(430, 400, 641, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.ad2.setFont(font)
        self.ad2.setStyleSheet("\n"
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
"}")
        self.ad2.setObjectName("ad2")
        self.ad3 = QtWidgets.QLineEdit(self.centralwidget)
        self.ad3.setGeometry(QtCore.QRect(430, 440, 641, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.ad3.setFont(font)
        self.ad3.setStyleSheet("\n"
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
"}")
        self.ad3.setObjectName("ad3")
        self.gwt = QtWidgets.QLineEdit(self.centralwidget)
        self.gwt.setGeometry(QtCore.QRect(330, 500, 113, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.gwt.setFont(font)
        self.gwt.setStyleSheet("\n"
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
"}")
        self.gwt.setObjectName("gwt")
        self.nwt = QtWidgets.QLineEdit(self.centralwidget)
        self.nwt.setGeometry(QtCore.QRect(580, 500, 113, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.nwt.setFont(font)
        self.nwt.setStyleSheet("\n"
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
"}")
        self.nwt.setObjectName("nwt")
        self.nop = QtWidgets.QLineEdit(self.centralwidget)
        self.nop.setGeometry(QtCore.QRect(830, 500, 81, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.nop.setFont(font)
        self.nop.setStyleSheet("\n"
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
"}")
        self.nop.setObjectName("nop")
        self.purity = QtWidgets.QLineEdit(self.centralwidget)
        self.purity.setGeometry(QtCore.QRect(1070, 500, 91, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.purity.setFont(font)
        self.purity.setStyleSheet("\n"
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
"}")
        self.purity.setObjectName("purity")
        self.principal = QtWidgets.QLineEdit(self.centralwidget)
        self.principal.setGeometry(QtCore.QRect(330, 560, 113, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.principal.setFont(font)
        self.principal.setStyleSheet("\n"
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
"}")
        self.principal.setObjectName("principal")
        self.interest = QtWidgets.QLineEdit(self.centralwidget)
        self.interest.setGeometry(QtCore.QRect(330, 620, 113, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.interest.setFont(font)
        self.interest.setStyleSheet("\n"
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
"}")
        self.interest.setObjectName("interest")
        self.intmonth = QtWidgets.QLineEdit(self.centralwidget)
        self.intmonth.setEnabled(True)
        self.intmonth.setGeometry(QtCore.QRect(690, 620, 113, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.intmonth.setFont(font)
        self.intmonth.setStyleSheet("\n"
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
"}")
        self.intmonth.setReadOnly(True)
        self.intmonth.setObjectName("intmonth")
        self.intcollected = QtWidgets.QLineEdit(self.centralwidget)
        self.intcollected.setGeometry(QtCore.QRect(420, 670, 101, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.intcollected.setFont(font)
        self.intcollected.setStyleSheet("")
        self.intcollected.setObjectName("intcollected")
        self.savebutton = QtWidgets.QPushButton(self.centralwidget)
        self.savebutton.setGeometry(QtCore.QRect(690, 720, 121, 51))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.savebutton.setFont(font)
        self.savebutton.setStyleSheet("QPushButton{\n"
"    \n"
"    \n"
"    background-color: #1d3557;\n"
"    border-radius:15px;\n"
"    color: rgb(241, 250, 238);\n"
"    border : 4px solid #a8dadc;\n"
"\n"
"\n"
"}\n"
"\n"
"QPushButton:hover\n"
"QPushButton:focus{\n"
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
"\n"
"")
        self.savebutton.setCheckable(False)
        self.savebutton.setAutoDefault(True)
        self.savebutton.setDefault(True)
        self.savebutton.setObjectName("savebutton")
        Pledge_Windoow.setCentralWidget(self.centralwidget)

        self.retranslateUi(Pledge_Windoow)
        QtCore.QMetaObject.connectSlotsByName(Pledge_Windoow)
        Pledge_Windoow.setTabOrder(self.pledgeno, self.pledgedate)
        Pledge_Windoow.setTabOrder(self.pledgedate, self.searchbar)
        Pledge_Windoow.setTabOrder(self.searchbar, self.address)
        Pledge_Windoow.setTabOrder(self.address, self.goldradio)
        Pledge_Windoow.setTabOrder(self.goldradio, self.silverradio)
        Pledge_Windoow.setTabOrder(self.silverradio, self.ad1)
        Pledge_Windoow.setTabOrder(self.ad1, self.ad2)
        Pledge_Windoow.setTabOrder(self.ad2, self.ad3)
        Pledge_Windoow.setTabOrder(self.ad3, self.gwt)
        Pledge_Windoow.setTabOrder(self.gwt, self.nwt)
        Pledge_Windoow.setTabOrder(self.nwt, self.nop)
        Pledge_Windoow.setTabOrder(self.nop, self.purity)
        Pledge_Windoow.setTabOrder(self.purity, self.principal)
        Pledge_Windoow.setTabOrder(self.principal, self.interest)
        Pledge_Windoow.setTabOrder(self.interest, self.intmonth)
        Pledge_Windoow.setTabOrder(self.intmonth, self.intcollected)
        Pledge_Windoow.setTabOrder(self.intcollected, self.savebutton)

    def retranslateUi(self, Pledge_Windoow):
        _translate = QtCore.QCoreApplication.translate
        Pledge_Windoow.setWindowTitle(_translate("Pledge_Windoow", "Pledge"))
        self.label.setText(_translate("Pledge_Windoow", "Name"))
        self.label_2.setText(_translate("Pledge_Windoow", "Date"))
        self.label_3.setText(_translate("Pledge_Windoow", "Article Description"))
        self.label_4.setText(_translate("Pledge_Windoow", "Loan Type"))
        self.label_5.setText(_translate("Pledge_Windoow", "Net wt"))
        self.label_6.setText(_translate("Pledge_Windoow", "Gross wt"))
        self.label_7.setText(_translate("Pledge_Windoow", "Address"))
        self.label_8.setText(_translate("Pledge_Windoow", "Pledge No"))
        self.label_9.setText(_translate("Pledge_Windoow", "NOP"))
        self.label_10.setText(_translate("Pledge_Windoow", "Purity"))
        self.label_11.setText(_translate("Pledge_Windoow", "Principal "))
        self.label_12.setText(_translate("Pledge_Windoow", "Interest"))
        self.label_13.setText(_translate("Pledge_Windoow", "Interest Collected"))
        self.label_14.setText(_translate("Pledge_Windoow", "Interest/month"))
        self.silverradio.setText(_translate("Pledge_Windoow", "Silver"))
        self.goldradio.setText(_translate("Pledge_Windoow", "gold"))
        self.savebutton.setText(_translate("Pledge_Windoow", "save"))


