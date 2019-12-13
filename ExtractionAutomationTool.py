# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ExtractionAutomationTool.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("* {\n"
"\n"
"background-color: white;\n"
"}\n"
"QTabBar::tab{\n"
"background-color:white;\n"
"height: 40px;\n"
"min-width: 50px;\n"
"width:150px;\n"
"color: #156abf;\n"
"\n"
"}\n"
"QTabBar::tab:selected {\n"
"background-color:#48a5e8;\n"
"border-top-right-radius: 4px;\n"
"border-top-left-radius: 4px;\n"
"color:white;\n"
"}\n"
"#infosGB,#delimiterGB{\n"
"border: 1px solid red;\n"
"}\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.tabs.setGeometry(QtCore.QRect(10, 0, 781, 591))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.tabs.setFont(font)
        self.tabs.setStyleSheet("border: Opx;")
        self.tabs.setTabsClosable(False)
        self.tabs.setObjectName("tabs")
        self.indexesTab = QtWidgets.QWidget()
        self.indexesTab.setMinimumSize(QtCore.QSize(100, 465))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.indexesTab.setFont(font)
        self.indexesTab.setStyleSheet("height : 50px;\n"
"")
        self.indexesTab.setObjectName("indexesTab")
        self.label = QtWidgets.QLabel(self.indexesTab)
        self.label.setGeometry(QtCore.QRect(170, 20, 411, 101))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color:#107ac7;\n"
"")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.startButton = QtWidgets.QPushButton(self.indexesTab)
        self.startButton.setGeometry(QtCore.QRect(600, 480, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.startButton.setFont(font)
        self.startButton.setStyleSheet("background-color:#107ac7;\n"
"color: white;\n"
"\n"
"")
        self.startButton.setObjectName("startButton")
        self.label_2 = QtWidgets.QLabel(self.indexesTab)
        self.label_2.setGeometry(QtCore.QRect(120, 110, 31, 31))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("assets/Webp.net-resizeimage.png"))
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QTextEdit(self.indexesTab)
        self.textEdit.setGeometry(QtCore.QRect(150, 110, 511, 101))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.delimiterGB = QtWidgets.QGroupBox(self.indexesTab)
        self.delimiterGB.setGeometry(QtCore.QRect(50, 330, 361, 111))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.delimiterGB.setFont(font)
        self.delimiterGB.setStyleSheet("color:#107ac7;")
        self.delimiterGB.setObjectName("delimiterGB")
        self.delimiterCB = QtWidgets.QComboBox(self.delimiterGB)
        self.delimiterCB.setGeometry(QtCore.QRect(240, 30, 101, 22))
        self.delimiterCB.setObjectName("delimiterCB")
        self.delimiterCB.addItem("")
        self.delimiterCB.addItem("")
        self.delimiterCB.addItem("")
        self.label_3 = QtWidgets.QLabel(self.delimiterGB)
        self.label_3.setGeometry(QtCore.QRect(10, 30, 221, 51))
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.infosGB = QtWidgets.QGroupBox(self.indexesTab)
        self.infosGB.setGeometry(QtCore.QRect(430, 230, 331, 131))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.infosGB.setFont(font)
        self.infosGB.setStyleSheet("color:#107ac7;")
        self.infosGB.setObjectName("infosGB")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.infosGB)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(40, 20, 261, 101))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.NETagsLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.NETagsLabel.setText("")
        self.NETagsLabel.setObjectName("NETagsLabel")
        self.horizontalLayout.addWidget(self.NETagsLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.OtherTagsLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.OtherTagsLabel.setText("")
        self.OtherTagsLabel.setObjectName("OtherTagsLabel")
        self.horizontalLayout_3.addWidget(self.OtherTagsLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_4.addWidget(self.label_9)
        self.UnkTagsLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.UnkTagsLabel.setText("")
        self.UnkTagsLabel.setObjectName("UnkTagsLabel")
        self.horizontalLayout_4.addWidget(self.UnkTagsLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.lineEdit = QtWidgets.QLineEdit(self.indexesTab)
        self.lineEdit.setGeometry(QtCore.QRect(70, 240, 181, 41))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.uploadFileButton = QtWidgets.QPushButton(self.indexesTab)
        self.uploadFileButton.setGeometry(QtCore.QRect(290, 240, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.uploadFileButton.setFont(font)
        self.uploadFileButton.setStyleSheet("border-right: 2px solid #107ac7;\n"
"border-bottom: 2px solid #107ac7;\n"
"color:#107ac7;\n"
"\n"
"")
        self.uploadFileButton.setObjectName("uploadFileButton")
        self.errorContainer = QtWidgets.QGroupBox(self.indexesTab)
        self.errorContainer.setGeometry(QtCore.QRect(470, 370, 301, 81))
        self.errorContainer.setStyleSheet("background-color:rgba(252, 90, 78,1);\n"
"border-top-right-radius: 8px;\n"
"border-top-left-radius: 8px;\n"
"border-bottom-right-radius: 8px;\n"
"border-bottom-left-radius: 8px;")
        self.errorContainer.setTitle("")
        self.errorContainer.setObjectName("errorContainer")
        self.label_4 = QtWidgets.QLabel(self.errorContainer)
        self.label_4.setGeometry(QtCore.QRect(20, 20, 31, 31))
        self.label_4.setStyleSheet("background-color:transparent;")
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("assets/icons8-erreur-26.png"))
        self.label_4.setObjectName("label_4")
        self.errorLabel = QtWidgets.QLabel(self.errorContainer)
        self.errorLabel.setGeometry(QtCore.QRect(70, 20, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.errorLabel.setFont(font)
        self.errorLabel.setStyleSheet("color:white;")
        self.errorLabel.setText("")
        self.errorLabel.setWordWrap(True)
        self.errorLabel.setObjectName("errorLabel")
        self.successContainer = QtWidgets.QGroupBox(self.indexesTab)
        self.successContainer.setGeometry(QtCore.QRect(80, 469, 361, 71))
        self.successContainer.setStyleSheet("background-color:#41fa50;\n"
"border-top-right-radius: 8px;\n"
"border-top-left-radius: 8px;\n"
"border-bottom-right-radius: 8px;\n"
"border-bottom-left-radius: 8px;\n"
"")
        self.successContainer.setTitle("")
        self.successContainer.setObjectName("successContainer")
        self.label_6 = QtWidgets.QLabel(self.successContainer)
        self.label_6.setGeometry(QtCore.QRect(60, 20, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color:white;")
        self.label_6.setObjectName("label_6")
        self.label_8 = QtWidgets.QLabel(self.successContainer)
        self.label_8.setGeometry(QtCore.QRect(10, 20, 31, 31))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap("assets/icons8-ok-30.png"))
        self.label_8.setObjectName("label_8")
        self.tabs.addTab(self.indexesTab, "")
        self.rechercheTab = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.rechercheTab.setFont(font)
        self.rechercheTab.setStyleSheet("*{\n"
"background-color:white;\n"
"}\n"
"")
        self.rechercheTab.setObjectName("rechercheTab")
        self.tabs.addTab(self.rechercheTab, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Corpus Sources Automation Tool"))
        self.label.setText(_translate("MainWindow", "Building HMM Data Sources"))
        self.startButton.setText(_translate("MainWindow", "Start Extraction"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:600; color:#3486b3;\">Please respect input file format</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:600; color:#3486b3;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:600;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">- </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Input file must be encoded with </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:600; color:#ff0000;\">Windows-1256 arabic encoding</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">.</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:600; color:#3486b3;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:600;\">  </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">- </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Input file must be formatted as follow: word [Tab] Tag.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  - Please choose a concistent file that contains meaningfull sentences for better model results.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  - Make sure that the file is well sentences delimited using one of available delimiters.</span></p></body></html>"))
        self.delimiterGB.setTitle(_translate("MainWindow", "Delimter :"))
        self.delimiterCB.setItemText(0, _translate("MainWindow", "---"))
        self.delimiterCB.setItemText(1, _translate("MainWindow", "***"))
        self.delimiterCB.setItemText(2, _translate("MainWindow", "</EOS>"))
        self.label_3.setText(_translate("MainWindow", "Choose sentences delimiter used in the file :"))
        self.infosGB.setTitle(_translate("MainWindow", "Infos :"))
        self.label_5.setText(_translate("MainWindow", "NE Tags :"))
        self.label_7.setText(_translate("MainWindow", "OTHER Tags :"))
        self.label_9.setText(_translate("MainWindow", "Unrecognized :"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Please choose a text ..."))
        self.uploadFileButton.setText(_translate("MainWindow", "Upload File"))
        self.label_6.setText(_translate("MainWindow", "Information extracted successfully !"))
        self.tabs.setTabText(self.tabs.indexOf(self.indexesTab), _translate("MainWindow", "Information Extractor"))
        self.tabs.setTabText(self.tabs.indexOf(self.rechercheTab), _translate("MainWindow", "Sources Edition"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
