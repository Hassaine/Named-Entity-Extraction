
from ExtractionAutomationTool import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import *
import re


class Gui_Controller(QObject):


    def __init__(self,gui:Ui_MainWindow):
        super().__init__()
        self.gui=gui
        self.INPUT_FILE = None



    def setup(self):
        self.gui.errorContainer.setVisible(False)
        self.gui.successContainer.setVisible(False)
        self.gui.uploadFileButton.clicked.connect(lambda: self.chooseFile())
        self.gui.startButton.clicked.connect(lambda:self.extractInformations())


    def chooseFile(self):
        fileName=QFileDialog.getOpenFileName(self.gui.centralwidget, "Open file", "../", "Txt Files(*.txt)")
        self.INPUT_FILE=fileName[0]
        self.gui.lineEdit.setText(fileName[0][fileName[0].rindex("/")+1:])


    def extractInformations(self):
        self.gui.errorContainer.setVisible(False)
        self.gui.successContainer.setVisible(False)
        if self.INPUT_FILE is None:
            self.gui.errorLabel.setText("Input File not specified")
            self.gui.errorContainer.setVisible(True)
            return

        try:
            lines=open(self.INPUT_FILE,"r",encoding="windows-1256").readlines()

            delimiter=self.gui.delimiterCB.currentText()

            seqtagFile=open(self.INPUT_FILE+"_SeqTags.txt","w",encoding="windows-1256")
            neTagFile=open(self.INPUT_FILE+"_NELexico.txt","w",encoding="windows-1256")
            sentence=""
            totalLines=0
            neTagNbr=0
            otherTagNbr=0
            for line in lines:
                if re.match(delimiter,re.sub("\s","",line)):
                    seqtagFile.write(sentence)
                    sentence=""
                    continue
                if not re.search(r"^.+\s+.+$",line):
                    print("Input File Format Error : File is not well formated")
                    print("\t",line)
                    self.gui.errorLabel.setText("IInput File Format Error : File is not well formated")
                    self.gui.errorContainer.setVisible(True)
                    return
                totalLines+=1
                parts=re.split(r"\s+",line)
                sentence+=parts[1]+" "
                if(parts[1]=="O"): otherTagNbr+=1
                if parts[1].upper() in ['PERSON','ORG','OTHER','LOC','DATE','OCLUE','DCLUE','LCLUE','PCLUE','PREP','PUNC','CONJ','NPREFIX','DEF']:
                    neTagFile.write(line)
                    neTagNbr+=1


            self.gui.NETagsLabel.setText(str(neTagNbr))
            self.gui.OtherTagsLabel.setText(str(otherTagNbr))
            self.gui.UnkTagsLabel.setText(str(totalLines-neTagNbr-otherTagNbr))
            seqtagFile.close()
            neTagFile.close()

            self.gui.successContainer.setVisible(True)

        except Exception as ex:
            print("Error reading file","\n\t",str(ex))
            return


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    controller = Gui_Controller(ui)
    controller.setup()
    MainWindow.show()
    sys.exit(app.exec_())







