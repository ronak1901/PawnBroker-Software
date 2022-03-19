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




class Ui_HistoryWindow(QMainWindow):

    def __init__(self,x):

        global dbPath
        dbPath = x

        super(Ui_HistoryWindow, self).__init__()
        self.setupUi(self)

        listofwidgets = [self.Name, self.details, self.table, self.dt, self.comboBox, self.totalAmount, self.totalInterestAmount, self.totalInterestPaid, self.totalDue,
                         self.selAmount, self.selInt, self.selIntPaid, self.selDue, self.label, self.label_5, self.label_6, self.label_7, self.label_10,
                         self.label_11, self.label_12, self.label_13, self.label_14, self.label_15, self.label_16, self.label_17]
        scaling(listofwidgets)

        self.dt.setDate(date.today())

        conn = sqlite3.connect(dbPath)

        # executing completer on line edit
        c = conn.cursor()
        c.execute("SELECT CustomerName FROM CustomerDetails")

        items = c.fetchall()
        customernames = []
        for item in items:
                customernames.append(item[0])

        # conn.commit()
        # conn.close()

        self.completer = QCompleter(customernames)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.Name.setCompleter(self.completer)

        def loadTableData(pledgeDetails):

                # loading pledge data in the table
                pledgeCount = len(pledgeDetails)
                self.table.setRowCount(pledgeCount)
                self.table.setColumnCount(12)

                self.table.setHorizontalHeaderLabels(('Months', 'Days', 'PledgeNo', 'Date', 'Article Desc', 'Amount',
                                                      'ROI', 'Interest', 'G.Wt', 'N.Wt', 'Released', 'Int Collected'))

                rowCount = 0
                for pledge in pledgeDetails:
                        article = pledge[2] + pledge[3] + pledge[4]
                        status = pledge[10]
                        interest = ""
                        relDateStr = ''
                        if status == "0":
                                relDateStr = pledge[8]

                        else:
                                relDateStr = self.dt.text()


                        pleDateStr = pledge[1]

                        pleDate = datetime.strptime(pleDateStr, "%d-%m-%Y")
                        relDate = datetime.strptime(relDateStr, "%d-%m-%Y")

                        diffDay = relDate - pleDate
                        diffDays = diffDay.days + 1
                        mon = int(diffDays / 30)
                        numDays = diffDays % 30

                        if status == "1":
                                p = float(pledge[5])
                                r = float(pledge[11])
                                t = float(diffDays / 30)

                                if mon == 0 and numDays <= 30:
                                        interest = p * r / 100

                                elif mon < 12:
                                        interest = (p * t * r) / 100

                                else:
                                        interest = p * (pow((1 + (r * 12 / 100)), (t / 12)))

                        self.table.setItem(rowCount, 0, QTableWidgetItem(str(mon)))
                        self.table.setItem(rowCount, 1, QTableWidgetItem(str(numDays)))
                        self.table.setItem(rowCount, 2, QTableWidgetItem(str(pledge[0])))
                        self.table.setItem(rowCount, 3, QTableWidgetItem(str(pledge[1])))
                        self.table.setItem(rowCount, 4, QTableWidgetItem(str(article)))
                        self.table.setItem(rowCount, 5, QTableWidgetItem(str(pledge[5])))
                        self.table.setItem(rowCount, 6, QTableWidgetItem(str(pledge[11])))
                        self.table.setItem(rowCount, 7, QTableWidgetItem(str(interest)))
                        self.table.setItem(rowCount, 8, QTableWidgetItem(str(pledge[6])))
                        self.table.setItem(rowCount, 9, QTableWidgetItem(str(pledge[7])))
                        self.table.setItem(rowCount, 10, QTableWidgetItem(str(pledge[8])))
                        self.table.setItem(rowCount, 11, QTableWidgetItem(str(pledge[9])))

                        rowCount += 1

        def fetchdata():
                conn = sqlite3.connect(dbPath)
                c = conn.cursor()
                # print("key event")
                if (self.Name.text() not in customernames):
                        # error
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText("Enter a Valid Name !!")
                        msg.exec_()

                else:
                        c.execute(
                                "SELECT FatherName, DoorNo, Street, City, Pincode, PhoneNo, ROWID FROM CustomerDetails WHERE CustomerName = (?)",
                                [self.Name.text()])
                        x = c.fetchall()
                        addr = list(x[0])
                        global rowid
                        rowid = addr[6]
                        # print(addr)

                        self.details.setText(
                                f"Father/Husband : {addr[0]} \n\n{addr[1]}, {addr[2]}, \n{addr[3]}, {addr[4]},\n\nPhoneNo : {addr[5]} ")
                        self.comboBox.setCurrentIndex(0)

                        c.execute(
                                "select 	PledgeNum , PledgeDate , AD1 , AD2 , AD3 , Amount , GWt , NWt , ReleaseDate , InterestCollected , Status , RateOfInterest ,AdvanceInterest from PledgeDetails where CustomerId = (?) and status = 1",
                                (rowid,))
                        # print(c.fetchall())
                        pledgeDetails = c.fetchall()
                        # print(pledgeDetails)
                        # pledgeCount = len(pledgeDetails)
                        totalPleAmount = 0
                        totalInterest = 0
                        totalIntCollected = 0
                        for pledge in pledgeDetails:
                                relDateStr = self.dt.text()
                                pleDateStr = pledge[1]
                                relDate = datetime.strptime(relDateStr, '%d-%m-%Y')
                                pleDate = datetime.strptime(pleDateStr, '%d-%m-%Y')

                                diffDay = relDate - pleDate
                                diffDays = diffDay.days + 1
                                mon = int(diffDays / 30)
                                numDays = diffDays % 30

                                p = float(pledge[5])
                                r = float(pledge[11])
                                t = float(diffDays / 30)
                                interestcollected = float(pledge[12])

                                if mon == 0 and numDays <= 30:
                                        interest = interestcollected
                                elif mon < 12:
                                        interest = (p * t * r) / 100
                                else:
                                        interest = p * (pow((1 + (r * 12 / 100)), (t / 12)))
                                totalPleAmount += p
                                totalInterest += interest
                                totalIntCollected += interestcollected

                        totalDueAmount = totalPleAmount + totalInterest - totalIntCollected
                        self.totalAmount.setText(str(totalPleAmount))
                        self.totalInterestAmount.setText(str(totalInterest))
                        self.totalInterestPaid.setText(str(totalIntCollected))
                        self.totalDue.setText(str(totalDueAmount))

                        loadTableData(pledgeDetails)

        self.Name.returnPressed.connect(fetchdata)

        def selectionchange():

                if (self.Name.text() not in customernames):
                        # error
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText("Enter a Valid Name !!")
                        msg.exec_()
                        return

                # print("inside function")
                # print(self.comboBox.currentText())
                currentSelection = self.comboBox.currentText()
                conn = sqlite3.connect(dbPath)
                c = conn.cursor()
                if (currentSelection == "Pending"):
                        # print("pending")
                        c.execute(
                                "select 	PledgeNum , PledgeDate , AD1 , AD2 , AD3 , Amount , GWt , NWt , ReleaseDate , InterestCollected , Status , RateOfInterest from PledgeDetails where CustomerId = (?) and status =1",
                                (rowid,))
                        # print(c.fetchall())
                        pledgeDetails = c.fetchall()
                        loadTableData(pledgeDetails)

                elif (currentSelection == "Released"):
                        # print("release")
                        c.execute(
                                "select 	PledgeNum , PledgeDate , AD1 , AD2 , AD3 , Amount , GWt , NWt , ReleaseDate , InterestCollected , Status , RateOfInterest from PledgeDetails where CustomerId = (?) and status =0",
                                (rowid,))
                        # print(c.fetchall())
                        pledgeDetails = c.fetchall()
                        loadTableData(pledgeDetails)

                elif (currentSelection == "All"):
                        # print("all")
                        c.execute(
                                "select 	PledgeNum , PledgeDate , AD1 , AD2 , AD3 , Amount , GWt , NWt , ReleaseDate , InterestCollected , Status , RateOfInterest from PledgeDetails where CustomerId = (?)",
                                (rowid,))
                        # print(c.fetchall())
                        pledgeDetails = c.fetchall()
                        loadTableData(pledgeDetails)

                conn.commit()
                conn.close()

        def handleItemClick():
                indices = self.table.selectionModel().selectedRows()
                selTotalAmount = 0
                selIntTotalAmount = 0
                selIntPaidAmount = 0
                selDueAmount = 0

                for index in indices:
                        # print("selected index is", index.row())
                        row = index.row()
                        if (self.table.item(row, 7).text() != ""):
                                amnt = float(self.table.item(row, 5).text())
                                intr = float(self.table.item(row, 7).text())
                                roi = float(self.table.item(row, 6).text())
                                adv = amnt * roi / 100
                                selTotalAmount += amnt
                                selIntTotalAmount += intr
                                selIntPaidAmount += adv

                selDueAmount = selTotalAmount + selIntTotalAmount - selIntPaidAmount
                self.selAmount.setText(str(selTotalAmount))
                self.selInt.setText(str(selIntTotalAmount))
                self.selIntPaid.setText(str(selIntPaidAmount))
                self.selDue.setText(str(selDueAmount))

        # print(self.comboBox)
        self.comboBox.currentIndexChanged.connect(selectionchange)
        self.table.itemClicked.connect(handleItemClick)

        conn.commit()
        conn.close()





    def setupUi(self, HistoryWindow):
        HistoryWindow.setObjectName("HistoryWindow")
        HistoryWindow.resize(1330, 810)
        HistoryWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        HistoryWindow.setFont(font)
        HistoryWindow.setStyleSheet("\n"
"\n"
"QMainWindow{\n"
"background: rgb(241, 250, 238);\n"
"}\n"
"\n"
"\n"
"QLineEdit{\n"
"\n"
"background: #a8dadc;\n"
"border: 2px solid rgb(29, 53, 87);\n"
"border-radius : 10px;\n"
"\n"
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
        self.centralwidget = QtWidgets.QWidget(HistoryWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 39, 191, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 310, 171, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(1010, 600, 71, 33))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(280, 600, 111, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(1130, 310, 131, 41))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("QComboBox{\n"
"\n"
"background: #a8dadc;\n"
"border: 2px solid rgb(29, 53, 87);\n"
"\n"
"\n"
"}\n"
"\n"
"QComboBox:focus{\n"
"\n"
"border: 2px solid #e63946;\n"
"}\n"
"")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.Name = QtWidgets.QLineEdit(self.centralwidget)
        self.Name.setGeometry(QtCore.QRect(232, 39, 641, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.Name.setFont(font)
        self.Name.setObjectName("Name")
        self.details = QtWidgets.QTextEdit(self.centralwidget)
        self.details.setEnabled(True)
        self.details.setGeometry(QtCore.QRect(230, 89, 651, 191))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.details.setFont(font)
        self.details.setMouseTracking(True)
        self.details.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        self.details.setReadOnly(True)
        self.details.setObjectName("details")
        self.dt = QtWidgets.QDateEdit(self.centralwidget)
        self.dt.setEnabled(True)
        self.dt.setDisplayFormat("dd-MM-yyyy")
        self.dt.setGeometry(QtCore.QRect(210, 310, 161, 31))
        self.dt.setReadOnly(True)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.dt.setFont(font)
        self.dt.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.dt.setDate(QtCore.QDate(1752, 9, 14))
        self.dt.setObjectName("dt")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(90, 720, 61, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(340, 720, 151, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(310, 660, 181, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(60, 659, 101, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.selAmount = QtWidgets.QLineEdit(self.centralwidget)
        self.selAmount.setGeometry(QtCore.QRect(170, 659, 113, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.selAmount.setFont(font)
        self.selAmount.setObjectName("selAmount")
        self.selInt = QtWidgets.QLineEdit(self.centralwidget)
        self.selInt.setGeometry(QtCore.QRect(490, 660, 113, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.selInt.setFont(font)
        self.selInt.setObjectName("selInt")
        self.selIntPaid = QtWidgets.QLineEdit(self.centralwidget)
        self.selIntPaid.setGeometry(QtCore.QRect(490, 720, 113, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.selIntPaid.setFont(font)
        self.selIntPaid.setObjectName("selIntPaid")
        self.selDue = QtWidgets.QLineEdit(self.centralwidget)
        self.selDue.setGeometry(QtCore.QRect(170, 720, 113, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.selDue.setFont(font)
        self.selDue.setObjectName("selDue")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(760, 660, 101, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(800, 720, 51, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.totalAmount = QtWidgets.QLineEdit(self.centralwidget)
        self.totalAmount.setGeometry(QtCore.QRect(870, 660, 113, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.totalAmount.setFont(font)
        self.totalAmount.setObjectName("totalAmount")
        self.totalInterestAmount = QtWidgets.QLineEdit(self.centralwidget)
        self.totalInterestAmount.setGeometry(QtCore.QRect(1190, 660, 113, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.totalInterestAmount.setFont(font)
        self.totalInterestAmount.setObjectName("totalInterestAmount")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(1040, 720, 141, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.totalInterestPaid = QtWidgets.QLineEdit(self.centralwidget)
        self.totalInterestPaid.setGeometry(QtCore.QRect(1190, 720, 113, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.totalInterestPaid.setFont(font)
        self.totalInterestPaid.setObjectName("totalInterestPaid")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(1010, 660, 171, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.totalDue = QtWidgets.QLineEdit(self.centralwidget)
        self.totalDue.setGeometry(QtCore.QRect(870, 720, 113, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.totalDue.setFont(font)
        self.totalDue.setObjectName("totalDue")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(30, 370, 1271, 201))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        self.table.setFont(font)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(False)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        HistoryWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(HistoryWindow)
        QtCore.QMetaObject.connectSlotsByName(HistoryWindow)




    def retranslateUi(self, HistoryWindow):
        _translate = QtCore.QCoreApplication.translate
        HistoryWindow.setWindowTitle(_translate("HistoryWindow", "History"))
        self.label.setText(_translate("HistoryWindow", "Customer Name"))
        self.label_5.setText(_translate("HistoryWindow", "Interest As On"))
        self.label_6.setText(_translate("HistoryWindow", "Total"))
        self.label_7.setText(_translate("HistoryWindow", "Selected"))
        self.comboBox.setItemText(0, _translate("HistoryWindow", "Pending"))
        self.comboBox.setItemText(1, _translate("HistoryWindow", "Released"))
        self.comboBox.setItemText(2, _translate("HistoryWindow", "All"))
        self.label_10.setText(_translate("HistoryWindow", "Due"))
        self.label_11.setText(_translate("HistoryWindow", "Interest Paid"))
        self.label_12.setText(_translate("HistoryWindow", "Interest Amount"))
        self.label_13.setText(_translate("HistoryWindow", "Amount"))
        self.label_14.setText(_translate("HistoryWindow", "Amount"))
        self.label_15.setText(_translate("HistoryWindow", "Due"))
        self.label_16.setText(_translate("HistoryWindow", "Interest Paid"))
        self.label_17.setText(_translate("HistoryWindow", "Interest Amount"))


