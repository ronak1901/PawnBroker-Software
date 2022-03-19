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



class Ui_ReleaseWindow(QMainWindow):


    def __init__(self,x):
        global dbPath
        dbPath = x

        super(Ui_ReleaseWindow, self).__init__()
        self.setupUi(self)

        listofwidgets = [self.pledgenum, self.amount, self.days, self.months, self.intercol, self.intamt, self.totaldue,
                         self.customerdet, self.ad, self.savebtn,
                         self.label, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6, self.label_7,
                         self.label_8, self.label_9, self.dt, self.listView]
        scaling(listofwidgets)


        self.dt.setDate(date.today())

        # self.dt.setMaximumDate(date.today())

        def pressPledge():
                conn = sqlite3.connect(dbPath)
                c = conn.cursor()
                pledgeNum = self.pledgenum.text()
                # c.execute('SELECT CustomerId from PledgeDetails WHERE PledgeNum = (?)',(pledgeNum,))
                # custList = c.fetchall()
                # customerIdList = []
                # for cust in custList:
                # 	customerIdList.append(cust[0])

                c.execute(
                        'SELECT PledgeDetails.CustomerId, PledgeDetails.PledgeDate , CustomerDetails.CustomerName,PledgeDetails.Amount from CustomerDetails , PledgeDetails where CustomerDetails.ROWID = PledgeDetails.CustomerId and PledgeNum = ? and PledgeDetails.Status = "1"',
                        [pledgeNum])
                global detailsList
                detailsList = c.fetchall()
                # print(detailsList)

                if (detailsList == []):
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText("Pledge Does not Exists/Released !!")
                        msg.exec_()

                for details in detailsList:
                        detailStr = pledgeNum + "   " + details[1] + "    " + details[2] + "    " + details[3]
                        self.listView.addItem(detailStr)
                # print(releaseList)

                # print(diffDays)

                # print("The type of the date is now", type(date_time_obj))
                # print("The date is", date_time_obj)

                # self.listView.
                self.listView.itemClicked.connect(Clicked)

                conn.commit()
                conn.close()

        def Clicked():
                list_index = self.listView.currentRow()

                cust = detailsList[list_index]
                custId = cust[0]

                self.listView.clear()
                # listItems = self.listView.items()

                conn = sqlite3.connect(dbPath)
                c = conn.cursor()

                c.execute('SELECT CustomerName , FatherName , City from CustomerDetails WHERE  ROWID = (?)', custId)
                details = c.fetchall()[0]
                # print(details)
                self.customerdet.setText(
                        f"Name : {details[0]} \n\nFather/Husband : {details[1]}\n\nCity : {details[2]}")

                c.execute(
                        'SELECT AD1,AD2,AD3,GWt,NWt,NOP,Amount,PledgeDate,RateOfInterest,AdvanceInterest from PledgeDetails where PledgeNum = (?)',
                        (self.pledgenum.text(),))
                articles = c.fetchall()[0]
                # print(ad)
                self.ad.setText(
                        f"{articles[0]}, {articles[1]}, {articles[2]}\nGWt : {articles[3]}\tNWt : {articles[4]}\nNOP : {articles[5]}")
                self.amount.setText(articles[6])

                relDateStr = self.dt.text()
                pleDateStr = articles[7]
                # print(relDateStr +"\t"+ pleDateStr)

                relDate = datetime.strptime(relDateStr, '%d-%m-%Y')
                # print(relDate)

                pleDate = datetime.strptime(pleDateStr, '%d-%m-%Y')
                # print(pleDate)

                diffDay = relDate - pleDate
                diffDays = diffDay.days + 1
                mon = int(diffDays / 30)
                numDays = diffDays % 30
                # print(mon)
                # print(numDays)
                self.months.setText(str(mon))
                self.days.setText(str(numDays))

                p = float(articles[6])
                r = float(articles[8])
                t = float(diffDays / 30)
                interestcollected = float(articles[9])

                if mon == 0 and numDays <= 30:
                        self.intamt.setText("0")
                        self.totaldue.setText(articles[6])

                elif mon < 12:
                        interest = (p * t * r) / 100
                        interest -= interestcollected
                        self.intamt.setText(str(interest))
                        self.totaldue.setText(str(p + interest))

                else:
                        ci = p * (pow((1 + (r * 12 / 100)), (t / 12)))
                        ci -= interestcollected
                        self.intamt.setText(str(ci))
                        self.totaldue.setText(str(p + ci))

                conn.commit()
                conn.close()

        self.pledgenum.returnPressed.connect(pressPledge)
        self.savebtn.clicked.connect(self.saverelease)


    def saverelease(self):
            global dbPath

            conn = sqlite3.connect(dbPath)
            c = conn.cursor()

            c.execute("UPDATE PledgeDetails SET Status = ?, InterestCollected = ?, ReleaseDate = ? WHERE PledgeNum = ?",
                      ("0", self.intercol.text(), self.dt.text(), self.pledgenum.text()))

            conn.commit()
            conn.close()

            # reset the window
            self.pledgenum.setText("")
            self.amount.setText("")
            self.days.setText("")
            self.months.setText("")
            self.intercol.setText("")
            self.intamt.setText("")
            self.totaldue.setText("")
            self.customerdet.setText("")
            self.ad.setText("")



    def setupUi(self, ReleaseWindow):
        ReleaseWindow.setObjectName("ReleaseWindow")
        ReleaseWindow.setEnabled(True)
        ReleaseWindow.resize(1330, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ReleaseWindow.sizePolicy().hasHeightForWidth())
        ReleaseWindow.setSizePolicy(sizePolicy)
        ReleaseWindow.setMinimumSize(QtCore.QSize(0, 0))
        ReleaseWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        ReleaseWindow.setAutoFillBackground(False)
        ReleaseWindow.setStyleSheet("QMainWindow{\n"
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
        self.centralwidget = QtWidgets.QWidget(ReleaseWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 60, 151, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(541, 620, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(51, 195, 90, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(950, 60, 131, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(531, 480, 161, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(51, 550, 201, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(51, 480, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(531, 550, 171, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.dt = QtWidgets.QDateEdit(self.centralwidget)
        self.dt.setGeometry(QtCore.QRect(400, 60, 151, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dt.sizePolicy().hasHeightForWidth())
        self.dt.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.dt.setFont(font)
        self.dt.setStyleSheet("")
        self.dt.setObjectName("dt")
        self.amount = QtWidgets.QLineEdit(self.centralwidget)
        self.amount.setEnabled(True)
        self.amount.setGeometry(QtCore.QRect(141, 480, 113, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amount.sizePolicy().hasHeightForWidth())
        self.amount.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.amount.setFont(font)
        self.amount.setReadOnly(True)
        self.amount.setObjectName("amount")
        self.intercol = QtWidgets.QLineEdit(self.centralwidget)
        self.intercol.setGeometry(QtCore.QRect(251, 550, 113, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.intercol.sizePolicy().hasHeightForWidth())
        self.intercol.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.intercol.setFont(font)
        self.intercol.setFrame(True)
        self.intercol.setObjectName("intercol")
        self.months = QtWidgets.QLineEdit(self.centralwidget)
        self.months.setEnabled(True)
        self.months.setGeometry(QtCore.QRect(731, 480, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.months.sizePolicy().hasHeightForWidth())
        self.months.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.months.setFont(font)
        self.months.setReadOnly(True)
        self.months.setObjectName("months")
        self.intamt = QtWidgets.QLineEdit(self.centralwidget)
        self.intamt.setEnabled(True)
        self.intamt.setGeometry(QtCore.QRect(731, 550, 113, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.intamt.sizePolicy().hasHeightForWidth())
        self.intamt.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.intamt.setFont(font)
        self.intamt.setReadOnly(True)
        self.intamt.setObjectName("intamt")
        self.totaldue = QtWidgets.QLineEdit(self.centralwidget)
        self.totaldue.setEnabled(True)
        self.totaldue.setGeometry(QtCore.QRect(731, 620, 113, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.totaldue.sizePolicy().hasHeightForWidth())
        self.totaldue.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.totaldue.setFont(font)
        self.totaldue.setReadOnly(True)
        self.totaldue.setObjectName("totaldue")
        self.savebtn = QtWidgets.QPushButton(self.centralwidget)
        self.savebtn.setGeometry(QtCore.QRect(451, 700, 111, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.savebtn.sizePolicy().hasHeightForWidth())
        self.savebtn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.savebtn.setFont(font)
        self.savebtn.setStyleSheet("")
        self.savebtn.setAutoDefault(False)
        self.savebtn.setDefault(True)
        self.savebtn.setObjectName("savebtn")
        self.days = QtWidgets.QLineEdit(self.centralwidget)
        self.days.setEnabled(True)
        self.days.setGeometry(QtCore.QRect(811, 480, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.days.sizePolicy().hasHeightForWidth())
        self.days.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.days.setFont(font)
        self.days.setReadOnly(True)
        self.days.setObjectName("days")
        self.ad = QtWidgets.QTextEdit(self.centralwidget)
        self.ad.setEnabled(True)
        self.ad.setGeometry(QtCore.QRect(271, 320, 641, 121))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ad.sizePolicy().hasHeightForWidth())
        self.ad.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.ad.setFont(font)
        self.ad.setReadOnly(True)
        self.ad.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.ad.setObjectName("ad")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(51, 360, 201, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.customerdet = QtWidgets.QTextEdit(self.centralwidget)
        self.customerdet.setEnabled(True)
        self.customerdet.setGeometry(QtCore.QRect(150, 122, 761, 181))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customerdet.sizePolicy().hasHeightForWidth())
        self.customerdet.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.customerdet.setFont(font)
        self.customerdet.setReadOnly(True)
        self.customerdet.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.customerdet.setObjectName("customerdet")
        self.pledgenum = QtWidgets.QLineEdit(self.centralwidget)
        self.pledgenum.setGeometry(QtCore.QRect(1070, 60, 121, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pledgenum.sizePolicy().hasHeightForWidth())
        self.pledgenum.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.pledgenum.setFont(font)
        self.pledgenum.setObjectName("pledgenum")
        self.listView = QtWidgets.QListWidget(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(940, 130, 341, 241))
        self.listView.setObjectName("listView")
        ReleaseWindow.setCentralWidget(self.centralwidget)

        QWidget.setTabOrder(self.pledgenum, self.listView)
        QWidget.setTabOrder(self.listView, self.dt)
        QWidget.setTabOrder(self.dt, self.intercol)
        QWidget.setTabOrder(self.intercol, self.savebtn)
        QWidget.setTabOrder(self.savebtn, self.customerdet)
        QWidget.setTabOrder(self.customerdet, self.ad)
        QWidget.setTabOrder(self.ad, self.amount)
        QWidget.setTabOrder(self.amount, self.intamt)
        QWidget.setTabOrder(self.intamt, self.totaldue)
        QWidget.setTabOrder(self.totaldue, self.months)
        QWidget.setTabOrder(self.months, self.days)

        self.retranslateUi(ReleaseWindow)
        QtCore.QMetaObject.connectSlotsByName(ReleaseWindow)
        # ReleaseWindow.setTabOrder(self.pledgenum, self.listView)
        # ReleaseWindow.setTabOrder(self.listView, self.dt)
        # ReleaseWindow.setTabOrder(self.dt, self.intercol)
        # ReleaseWindow.setTabOrder(self.intercol, self.savebtn)
        # ReleaseWindow.setTabOrder(self.savebtn, self.totaldue)
        # ReleaseWindow.setTabOrder(self.totaldue, self.intamt)
        # ReleaseWindow.setTabOrder(self.intamt, self.days)
        # ReleaseWindow.setTabOrder(self.days, self.ad)
        # ReleaseWindow.setTabOrder(self.ad, self.customerdet)
        # ReleaseWindow.setTabOrder(self.customerdet, self.amount)
        # ReleaseWindow.setTabOrder(self.amount, self.months)


    def retranslateUi(self, ReleaseWindow):
        _translate = QtCore.QCoreApplication.translate
        ReleaseWindow.setWindowTitle(_translate("ReleaseWindow", "Release"))
        self.label.setText(_translate("ReleaseWindow", "Release Date"))
        self.label_2.setText(_translate("ReleaseWindow", "Total Due"))
        self.label_3.setText(_translate("ReleaseWindow", "Details"))
        self.label_4.setText(_translate("ReleaseWindow", "Pledge No"))
        self.label_6.setText(_translate("ReleaseWindow", "months / days"))
        self.label_7.setText(_translate("ReleaseWindow", "Interest Collected"))
        self.label_8.setText(_translate("ReleaseWindow", "Amount"))
        self.label_9.setText(_translate("ReleaseWindow", "Interest Amount"))
        self.savebtn.setText(_translate("ReleaseWindow", "Save"))
        self.label_5.setText(_translate("ReleaseWindow", "Article description"))


