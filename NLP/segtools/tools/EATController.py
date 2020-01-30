
from ExtractionAutomationTool import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QComboBox, QFileDialog, QHBoxLayout, QInputDialog, QLabel, QLineEdit, QPushButton, QScrollArea, QTableWidget, QTableWidgetItem, QWidget
from PyQt5.QtCore import *
import re,traceback,threading
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) # Up to NLP directory
sys.path.append(parentdir)
sys.path.append(parentdir+"\\model")
import staticContent
from staticContent import *
from random import randrange

TAGGS_TO_ADD=[]
Equivalence={}
BASE_CONTEXT_DIRECTORY=parentdir+"\\corpus\\contexts"
CONTENT_DELIMITERS={"<H>":"hadith","<D>":"diverse"} # this is a liste of choosen delimiters not for sentences but for text, <H> is Hadith delimiter
class Gui_Controller(QObject):


    def __init__(self,gui:Ui_MainWindow):
        super().__init__()
        self.gui=gui
        self.INPUT_FILE = None
        self.NE_TAGS=load_ne_tag_labels()
        self.newLines=[]



    def setup(self):
        self.gui.errorContainer.setVisible(False)
        self.gui.successContainer.setVisible(False)
        self.gui.infosGB.setVisible(False)
        self.gui.confirmButton.setVisible(False)
        self.gui.scrollArea.setVisible(False)
        self.gui.uploadFileButton.clicked.connect(lambda: self.chooseFile())
        self.gui.startButton.clicked.connect(lambda:self.extractInformations())
        self.gui.confirmButton.clicked.connect(lambda:self.writeNewTags())
                # TAB 2
        self.gui.confirm_new_nameButton.clicked.connect(lambda:self.update_new_ne_name())
        self.gui.undo_selectedButton.clicked.connect(lambda:self.remove_added_tag())
        self.gui.search_wordButton.clicked.connect(lambda:self.searchWord())
        self.gui.confirm_allButton.clicked.connect(lambda:self.submitChanges())


    def chooseFile(self):
        fileName=QFileDialog.getOpenFileName(self.gui.centralwidget, "Open file", "../", "Txt Files(*.txt)")
        self.INPUT_FILE=fileName[0]
        self.gui.lineEdit.setText(fileName[0][fileName[0].rindex("/")+1:])


    def extractInformations(self):
        self.gui.errorContainer.setVisible(False)
        self.gui.successContainer.setVisible(False)
        self.gui.infosGB.setVisible(False)
        if self.INPUT_FILE is None:
            self.gui.errorLabel.setText("Input File not specified")
            self.gui.errorContainer.setVisible(True)
            return
        self.newLines = []
        self.all_lines=[]
        TAGGS_TO_ADD=[]
        Equivalence={}
        try:
            lines=open(self.INPUT_FILE,"r",encoding="windows-1256").readlines()

            delimiter=self.gui.delimiterCB.currentText()
            base=parentdir+"\\corpus\sources\\"
            seqtagFile=open(base+"transition\\"+self.INPUT_FILE[self.INPUT_FILE.rindex("/")+1:].replace(".txt","")+"_SeqTags.txt","w",encoding="windows-1256")
            neTagFile=open(base+"emission\\"+self.INPUT_FILE[self.INPUT_FILE.rindex("/")+1:].replace(".txt","")+"_NELexicon.txt","w",encoding="windows-1256")
            sentence=""
            text=""
            contextTexts={}
            totalLines=0
            neTagNbr=0
            otherTagNbr=0
            for line in lines:
                line=line.upper()
                totalLines += 1
                if re.sub("\s+","",line)==delimiter:
                    seqtagFile.write(sentence+"\n")
                    sentence=""
                    continue
                
                trimmedLine=re.sub("\s+","",line)
                if  trimmedLine in CONTENT_DELIMITERS:
                    if not CONTENT_DELIMITERS[trimmedLine] in contextTexts:
                        contextTexts[CONTENT_DELIMITERS[trimmedLine]]=[]
                    contextTexts[CONTENT_DELIMITERS[trimmedLine]].append(text+" \n")

                    seqtagFile.write(sentence+"\n")
                    sentence=""
                    text=""
                    continue

                if not re.search(r"^.+\s+.+$",line):
                    print("Input File Format Error : File is not well formated")
                    print("\t",line)
                    self.gui.errorLabel.setText("IInput File Format Error : File is not well formated, (Line "+str(totalLines)+")")
                    self.gui.errorContainer.setVisible(True)
                    return
                self.all_lines.append(line)
                parts=re.split(r"\s+",line)
                if parts[1] == "O":
                    line = re.sub("\tO", "\tOTHER", line)
                    parts = re.split(r"\s+", line)
                sentence+=parts[1]+" "
                if parts[1].upper() in self.NE_TAGS or parts[1].upper() in ["O","OTHER"]:

                    neTagFile.write(line)
                    neTagNbr+=1
                elif parts[1].upper() == "O" or parts[1].upper() =="OTHER":
                    otherTagNbr += 1
                else:
                    self.newLines.append(line)

                text+=parts[0]+" "

            self.gui.infosGB.setVisible(True)
            self.gui.NETagsLabel.setText(str(neTagNbr))
            self.gui.OtherTagsLabel.setText(str(totalLines))
            self.gui.UnkTagsLabel.setText(str(len(self.newLines)))
            

                #showing new unrecognized tags
            if len(self.newLines)>0:
                self.gui.confirmButton.setVisible(True)
                #self.gui.horizontalLayout_2.setVisible(True)
                new_tags=[]
                for newTag in self.newLines:
                    
                    self.gui.newWordsLabel.setText(self.gui.newWordsLabel.text()+newTag+"\n")
                    tags=[el for el in re.split("\s+",newTag)[1:] if el!=""]
                    for el in tags:

                        new_tags.append(el)

                
                new_tags=set(new_tags)    
                print(new_tags)
                if len(new_tags) >0:
                    for tag in new_tags:
                        button=QPushButton("+ "+tag)
                        button.setObjectName("+ "+tag)
                        button.setStyleSheet("background-color:#107ac7; color: white; font-weight:bold;")
                        button.clicked.connect(self.new_new_tag_choosed)
                        
                        self.gui.newTagscontainer.addWidget(button) 

                    self.gui.scrollArea.setVisible(True)       
    
            seqtagFile.close()
            neTagFile.close()
                # Create text corpus
            if bool(contextTexts):
                for context in contextTexts:
                    dirs=list(os.walk(BASE_CONTEXT_DIRECTORY))[0][1]
                    if context not in dirs:
                        os.mkdir(os.path.abspath(BASE_CONTEXT_DIRECTORY+"\\"+context))

                    f=open(BASE_CONTEXT_DIRECTORY+"\\"+context+"\\"+context+"_texts.txt","a",encoding="windows-1256")
                    for text in contextTexts[context]:
                        f.write(text)
                    f.close()


            self.gui.successContainer.setVisible(True)

        except Exception as ex:
            print("Error reading file","\n\t",str(ex))
            traceback.print_exc()
            return

    def new_new_tag_choosed(self):

        self.sender().setStyleSheet("background-color:rgb(180,180,180); color:white;")
        tag=self.sender().text().replace("+ ","")
        TAGGS_TO_ADD.append(tag)
        Equivalence[tag]=""
        if tag not in [self.gui.tags_to_addCombobox.itemText(i) for i in range(self.gui.tags_to_addCombobox.count()) ]:
            self.gui.tags_to_addCombobox.addItem(tag)

    def writeNewTags(self):

        base = parentdir + "\\corpus\sources\\"
        neTagFile = open(base + "emission\\" + self.INPUT_FILE[self.INPUT_FILE.rindex("/") + 1:].replace(".txt",
                                            "") + "_NELexicon.txt","a", encoding="windows-1256")
        for line in self.newLines:
            tag=re.split("\s+",line)[1]
            word=re.split("\s+",line)[0]
            if tag in Equivalence and Equivalence[tag]!="":
                neTagFile.write(word+"\t"+Equivalence[tag]+"\n")
            elif(tag in TAGGS_TO_ADD):
                neTagFile.write(line)

        neTagFile.close()
        self.NE_TAGS=self.NE_TAGS+TAGGS_TO_ADD

        #NE_TAG_lABELS=self.NE_TAGS
        try:
            save_ne_tag_labels(self.NE_TAGS)
        except Exception as e:
            print(e)

                # TAB 2
    def update_new_ne_name(self):
        self.gui.update_success_label.setVisible(True)
        self.gui.rename_tag_edit.setStyleSheet("")
        old_tag=str(self.gui.tags_to_addCombobox.currentText())
        new_tag=self.gui.rename_tag_edit.text()
        if new_tag=="":
            self.gui.rename_tag_edit.setStyleSheet("Border: 3px solid red;")
            return
        Equivalence[old_tag]=new_tag.replace(" ","")   
        TAGGS_TO_ADD.remove(old_tag) 
        self.gui.rename_tag_edit.clear()
        self.gui.update_success_label.setVisible(True)


    def remove_added_tag(self):
        tag_to_remove=str(self.gui.tags_to_addCombobox.currentText())  
        TAGGS_TO_ADD.remove(tag_to_remove)
        del Equivalence[tag_to_remove]  

        self.gui.tags_to_addCombobox.removeItem(self.gui.tags_to_addCombobox.currentIndex())
        targetsBtn=[ self.gui.newTagscontainer.itemAt(i).widget() for i in range(self.gui.newTagscontainer.count()) if tag_to_remove in self.gui.newTagscontainer.itemAt(i).widget().objectName()]
        if len(targetsBtn)>0:
            targetsBtn[0].setStyleSheet("background-color:#107ac7; color: white;")

    def searchWord(self):
        self.tableW=None
        for i in reversed(range(self.gui.editvbox.count())):
            self.gui.editvbox.itemAt(i).widget().setParent(None)

        word=self.gui.searcch_word_edit.text()
        if word=="":
            return
        
        
        liste_lines=[line for line in self.all_lines if line.startswith(word)]
        if len(liste_lines)==0:
            print("No line containing the specified word is found.")
            return
        liste_lines=set(liste_lines)
        self.tableW = QTableWidget()
        self.tableW.setColumnCount(2)
        self.tableW.setHorizontalHeaderLabels(
                ['Word', 'Tags'])
        self.tableW.setRowCount(len(liste_lines))  
        i = 0
        for line in liste_lines:
                words=re.split("\s+",line)

                item=QTableWidgetItem(""+word)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableW.setItem(i,0,item)
                self.tableW.setItem(i,1,QTableWidgetItem(""+words[1]))

                i += 1

        #self.tableW.cellClicked.connect(self.onCellClick)

        self.gui.editvbox.addWidget(self.tableW)  

    def submitChanges(self):

        if self.tableW is None:
            return

        for i in range(self.tableW.rowCount()):
            new_line=self.tableW.item(i,0)+"\t"+self.tableW.item(i,1)
            self.all_lines[i]=new_line
            print(self.all_lines[i])




        

class MyWindow(QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.table = QTableWidget(5,5)
        self.table.setHorizontalHeaderLabels(['1', '2', '3', '4', '5'])
        self.table.setVerticalHeaderLabels(['1', '2', '3', '4', '5'])
        self.table.horizontalHeader().sectionDoubleClicked.connect(self.changeHorizontalHeader)

        layout = QHBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def changeHorizontalHeader(self, index):
        oldHeader = self.table.horizontalHeaderItem(index).text()
        newHeader, ok = QInputDialog.getText(self,
                                                      'Change header label for column %d' % index,
                                                      'Header:',
                                                       QLineEdit.Normal,
                                                       oldHeader)
        print(self.table.item(0,0).text())                                               
        if ok:
            self.table.horizontalHeaderItem(index).setText(newHeader)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)

#     main = MyWindow()
#     main.show()

#     sys.exit(app.exec_())

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

'''
f=open("WIKIFANE_corpus_all.txt","r",encoding="windows-1256")
d=open("WIKIFANE_corpus_all_pure.txt","w",encoding="windows-1256")
cpt=0
for line in f:
    line=line.upper()
    if line=="\n":
        d.write("<D>\n")
        continue
    if not re.match("[\")$£%:(*?!'/\\,.؟]\sO",line):
        d.write(line)

d.close()
f.close()
'''








