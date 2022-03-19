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
from pledge_window import Ui_Pledge_Windoow
from release_window import  Ui_ReleaseWindow
from addnewcustomer_window import  Ui_CutstomerWindow
from newdb_window import  Ui_Form
from history_window import Ui_HistoryWindow
from findcustomer_window import  Ui_FindCustWindow
from dailyreport_window import  Ui_ReportWindow
from scaling import scaling



class Ui_MainWindow(QMainWindow):

    global dbPath


    def __init__(self):
        super(Ui_MainWindow, self).__init__()

        self.selectingdabatabse()
        self.setupUi(self)

        listofwidgets = [self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4, self.createnewdb, self.mdiArea]
        scaling(listofwidgets)



        self.showMaximized()

        self.pushButton.clicked.connect(self.pledgewin)
        self.pushButton_2.clicked.connect(self.releasewin)
        self.pushButton_3.clicked.connect(self.addnewwin)
        self.pushButton_4.clicked.connect(self.historywin)
        self.createnewdb.clicked.connect(self.newdbwin)
        self.actionDailyReport.triggered.connect(self.onReportButtonClick)
        self.actionEditCustomer.triggered.connect(self.onEditCustomerButtonClick)
        self.actionEditPledge.triggered.connect(self.onEditPledgeButtonClick)
        self.actionFindCustomer.triggered.connect(self.onFindCustomerButtonClick)

        # self.showMaximized()


    def selectingdabatabse(self):
        global dbPath
        filename = QFileDialog.getOpenFileName(self, "Select Database", "D:\Software", "db files (*.db)")
        if filename[0] == '':
            self.selectingdabatabse()

        elif filename:
            # print(filename[0])
            dbPath = filename[0]



    def newdbwin(self):
        sub = Ui_Form(dbPath)
        self.mdiArea.addSubWindow(sub)
        self.mdiArea.closeActiveSubWindow()
        sub.show()

        self.mdiArea.cascadeSubWindows()





    def pledgewin(self):
        sub = Ui_Pledge_Windoow(dbPath)
        self.mdiArea.addSubWindow(sub)
        self.mdiArea.closeActiveSubWindow()
        sub.show()

        self.mdiArea.tileSubWindows()

        sub.savebutton.clicked.connect(sub.savepledge)




    def releasewin(self):
        sub = Ui_ReleaseWindow(dbPath)
        self.mdiArea.addSubWindow(sub)
        self.mdiArea.closeActiveSubWindow()
        sub.show()

        self.mdiArea.tileSubWindows()



    def addnewwin(self):
        sub = Ui_CutstomerWindow(dbPath)
        self.mdiArea.addSubWindow(sub)
        self.mdiArea.closeActiveSubWindow()
        sub.show()

        self.mdiArea.tileSubWindows()
        sub.savebutton.clicked.connect(sub.save_data)
        sub.name.returnPressed.connect(sub.checkName)



    def historywin(self):
        sub = Ui_HistoryWindow(dbPath)
        self.mdiArea.addSubWindow(sub)
        self.mdiArea.closeActiveSubWindow()
        sub.show()

        self.mdiArea.tileSubWindows()





    def onEditCustomerButtonClick(self):
        sub = Ui_CutstomerWindow(dbPath)
        self.mdiArea.addSubWindow(sub)
        self.mdiArea.closeActiveSubWindow()
        sub.show()

        self.mdiArea.tileSubWindows()
        sub.savebutton.clicked.connect(sub.edit_data)
        sub.name.returnPressed.connect(sub.fill_data)




    def onEditPledgeButtonClick(self):
        sub = Ui_Pledge_Windoow(dbPath)
        self.mdiArea.addSubWindow(sub)
        self.mdiArea.closeActiveSubWindow()
        sub.show()

        self.mdiArea.tileSubWindows()
        sub.pledgeno.returnPressed.connect(sub.showpledgedata)
        sub.savebutton.clicked.connect(sub.pledgeEdit)




    def onFindCustomerButtonClick(self):
        sub = Ui_FindCustWindow(dbPath)
        self.mdiArea.addSubWindow(sub)
        self.mdiArea.closeActiveSubWindow()
        sub.show()

        self.mdiArea.tileSubWindows()



    def onReportButtonClick(self):
        sub = Ui_ReportWindow(dbPath)
        self.mdiArea.addSubWindow(sub)
        self.mdiArea.closeActiveSubWindow()
        sub.show()

        self.mdiArea.tileSubWindows()






    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 990)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        MainWindow.setStyleSheet("QMainWindow{\n"
                                 "background : #a8dadc;\n"
                                 "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea.setGeometry(QtCore.QRect(390, 40, 1330, 850))
        self.mdiArea.setToolTip("")
        self.mdiArea.setStyleSheet("")
        self.mdiArea.setObjectName("mdiArea")
        self.createnewdb = QtWidgets.QPushButton(self.centralwidget)
        self.createnewdb.setGeometry(QtCore.QRect(40, 684, 321, 61))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.createnewdb.sizePolicy().hasHeightForWidth())
        self.createnewdb.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.createnewdb.setFont(font)
        self.createnewdb.setStyleSheet("QPushButton{\n"
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
                                       "\n"
                                       "")
        self.createnewdb.setAutoDefault(True)
        self.createnewdb.setDefault(False)
        self.createnewdb.setObjectName("createnewdb")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 198, 171, 61))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton{\n"
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
                                      "\n"
                                      "")
        self.pushButton.setAutoDefault(True)
        self.pushButton.setDefault(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 314, 171, 61))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton{\n"
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
                                        "\n"
                                        "")
        self.pushButton_2.setAutoDefault(True)
        self.pushButton_2.setDefault(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 423, 171, 61))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("QPushButton{\n"
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
                                        "\n"
                                        "")
        self.pushButton_3.setAutoDefault(True)
        self.pushButton_3.setDefault(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(100, 540, 171, 61))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("QPushButton{\n"
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
                                        "\n"
                                        "")
        self.pushButton_4.setAutoDefault(True)
        self.pushButton_4.setDefault(False)
        self.pushButton_4.setObjectName("pushButton_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.toolBar.setFont(font)
        self.toolBar.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.toolBar.setToolTip("")
        self.toolBar.setToolTipDuration(-15)
        self.toolBar.setAutoFillBackground(False)
        self.toolBar.setStyleSheet("color: rgb(241, 250, 238);\n"
                                   "background-color: rgb(29, 53, 87);")
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionDailyReport = QtWidgets.QAction(MainWindow)
        self.actionDailyReport.setObjectName("actionDailyReport")
        self.actionEditCustomer = QtWidgets.QAction(MainWindow)
        self.actionEditCustomer.setObjectName("actionEditCustomer")
        self.actionFindCustomer = QtWidgets.QAction(MainWindow)
        self.actionFindCustomer.setObjectName("actionFindCustomer")
        self.actionEditPledge = QtWidgets.QAction(MainWindow)
        self.actionEditPledge.setObjectName("actionEditPledge")
        self.toolBar.addAction(self.actionDailyReport)
        self.toolBar.addAction(self.actionEditCustomer)
        self.toolBar.addAction(self.actionFindCustomer)
        self.toolBar.addAction(self.actionEditPledge)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)




    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.createnewdb.setText(_translate("MainWindow", "NEW FINANCIAL YEAR"))
        self.pushButton.setText(_translate("MainWindow", "PLEDGE"))
        self.pushButton_2.setText(_translate("MainWindow", "RELEASE"))
        self.pushButton_3.setText(_translate("MainWindow", "ADD NEW"))
        self.pushButton_4.setText(_translate("MainWindow", "HISTORY"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionDailyReport.setText(_translate("MainWindow", "DailyReport"))
        self.actionDailyReport.setToolTip(_translate("MainWindow", "<html><head/><body><p>generate report</p><p><br/></p></body></html>"))
        self.actionDailyReport.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionEditCustomer.setText(_translate("MainWindow", "EditCustomer"))
        self.actionFindCustomer.setText(_translate("MainWindow", "FindCustomer"))
        self.actionEditPledge.setText(_translate("MainWindow", "EditPledge"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())



app = QApplication(sys.argv)
UIWindow = Ui_MainWindow()
app.exec_()
