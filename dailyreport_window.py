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



class Ui_ReportWindow(QMainWindow):

    def __init__(self,x):
        global dbPath
        dbPath = x

        super(Ui_ReportWindow, self).__init__()
        self.setupUi(self)

        listofwidgets = [self.date, self.displaybutton, self.table, self.printbutton, self.label_2]
        scaling(listofwidgets)

        self.date.setDate(date.today())
        # self.date.setMaximumDate(date.today())

        self.displaybutton.clicked.connect(self.display)
        self.printbutton.clicked.connect(self.preview)

    def display(self):
            global dbPath

            if (self.date.date().toPyDate() > date.today()):
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Enter a Valid date !!")
                    msg.exec_()

            else:

                    self.table.clear()

                    conn = sqlite3.connect(dbPath)
                    c = conn.cursor()

                    self.table.setColumnCount(12)
                    self.table.setHorizontalHeaderLabels(("Amount", "Name", "P.Date", "", "P.No", "Name", "Father",
                                                          "City", "Article", "GWt", "Amount", "R.Date"))
                    c.execute(
                            'SELECT CustomerDetails.CustomerName, PledgeDetails.PledgeDate, PledgeDetails.Amount FROM CustomerDetails, PledgeDetails WHERE PledgeDetails.Status = "0" and PledgeDetails.ReleaseDate = ? and CustomerDetails.ROWID = PledgeDetails.CustomerId',
                            [self.date.text()])

                    rdet = c.fetchall()
                    # print(rdet)
                    releasedet = []

                    for r in rdet:
                            releasedet.append(r)

                    # print(releasedet)
                    c.execute(
                            'SELECT PledgeDetails.PledgeNum , CustomerDetails.CustomerName, CustomerDetails.FatherName, CustomerDetails.City, PledgeDetails.AD1,PledgeDetails.AD2, PledgeDetails.AD3, PledgeDetails.GWt, PledgeDetails.Amount from CustomerDetails,PledgeDetails WHERE PledgeDetails.Status = "1" and PledgeDetails.PledgeDate = ? and CustomerDetails.ROWID = PledgeDetails.CustomerId',
                            [self.date.text()])

                    pdet = c.fetchall()
                    pledgedet = []

                    for p in pdet:
                            pledgedet.append(p)

                    if (len(releasedet) > len(pledgedet)):
                            rownum = len(releasedet)

                    else:
                            rownum = len(pledgedet)

                    self.table.setRowCount(rownum)

                    if (len(releasedet) != 0):
                            rowCount = 0
                            for r in releasedet:
                                    self.table.setItem(rowCount, 0, QTableWidgetItem(str(r[2])))
                                    self.table.setItem(rowCount, 1, QTableWidgetItem(str(r[0])))
                                    self.table.setItem(rowCount, 2, QTableWidgetItem(str(r[1])))
                                    rowCount += 1

                    if (len(pledgedet) != 0):

                            rowCount = 0
                            for p in pledgedet:
                                    self.table.setItem(rowCount, 4, QTableWidgetItem(str(p[0])))
                                    self.table.setItem(rowCount, 5, QTableWidgetItem(str(p[1])))
                                    self.table.setItem(rowCount, 6, QTableWidgetItem(str(p[2])))
                                    self.table.setItem(rowCount, 7, QTableWidgetItem(str(p[3])))
                                    self.table.setItem(rowCount, 8,
                                                       QTableWidgetItem(str(p[4] + " " + p[5] + " " + p[6])))
                                    self.table.setItem(rowCount, 9, QTableWidgetItem(str(p[7])))
                                    self.table.setItem(rowCount, 10, QTableWidgetItem(str(p[8])))
                                    rowCount += 1

                    conn.commit()
                    conn.close()

    def preview(self):
            printer = QPrinter(QPrinter.HighResolution)
            # dialog = QPrintDialog(printer,self)
            previewDialog = QPrintPreviewDialog(printer, self)
            previewDialog.paintRequested.connect(self.printreport)
            previewDialog.exec_()

    def printreport(self, printer):
            global dbPath

            document = QtGui.QTextDocument()
            font = document.defaultFont()
            font.setPointSize(10)
            font.setFamily("SansSerif")
            document.setDefaultFont(font)

            cursor = QtGui.QTextCursor(document)
            cursor.insertText(self.date.text())
            table = cursor.insertTable(self.table.rowCount() + 1, self.table.columnCount())
            # x = table.cellAt(1,0)
            # cells = x.format()
            # cell = cells.toTableCellFormat()
            # cell.setBorderStyle(0)
            # cell.setPadding(0)
            # cell.setBorder(0)
            # x.setFormat(cell)
            # frame = cursor.currentFrame()
            # frameFormat = frame.frameFormat()
            # frameFormat.setBorderStyle(3)
            #
            # frame.setFrameFormat(frameFormat)
            #

            headers = [" Amt ", " Name", " P.Date", " ", " P.No", " Name", " Father", " City", " Article", " GWt",
                       " Amt ", " R.Date"]

            for header in headers:
                    cursor.insertText(header)
                    cursor.movePosition(QtGui.QTextCursor.NextCell)

            for row in range(table.rows()):
                    for col in range(table.columns()):
                            it = self.table.item(row, col)
                            if it is not None:
                                    cursor.insertText(" " + it.text())
                            cursor.movePosition(QtGui.QTextCursor.NextCell)

                    # if dialog.exec_() == QPrintDialog.Accepted:
                    document.print_(printer)







    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 820)
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
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.date = QtWidgets.QDateEdit(self.centralwidget)
        self.date.setGeometry(QtCore.QRect(180, 50, 151, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.date.setFont(font)
        self.date.setStyleSheet("\n"
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
        self.date.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.date.setObjectName("date")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(100, 50, 51, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color:transparent;")
        self.label_2.setObjectName("label_2")
        self.displaybutton = QtWidgets.QPushButton(self.centralwidget)
        self.displaybutton.setGeometry(QtCore.QRect(410, 40, 211, 51))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.displaybutton.setFont(font)
        self.displaybutton.setStyleSheet("QPushButton{\n"
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
        self.displaybutton.setCheckable(False)
        self.displaybutton.setAutoDefault(True)
        self.displaybutton.setDefault(True)
        self.displaybutton.setObjectName("displaybutton")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(45, 111, 1211, 691))
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.printbutton = QtWidgets.QPushButton(self.centralwidget)
        self.printbutton.setGeometry(QtCore.QRect(660, 40, 111, 51))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.printbutton.setFont(font)
        self.printbutton.setStyleSheet("QPushButton{\n"
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
        self.printbutton.setCheckable(False)
        self.printbutton.setAutoDefault(True)
        self.printbutton.setDefault(True)
        self.printbutton.setObjectName("printbutton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Daily Report"))
        self.label_2.setText(_translate("MainWindow", "Date"))
        self.displaybutton.setText(_translate("MainWindow", "Display Report "))
        self.printbutton.setText(_translate("MainWindow", "Print"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
