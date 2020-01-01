
from ExtractionAutomationTool import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QPushButton,QLabel,QScrollArea
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

TAGGS_TO_ADD=[]
BASE_CONTEXT_DIRECTORY=parentdir+"\\corpus\\contexts"
CONTENT_DELIMITERS={"<H>":"hadith","<D>":"diverse"} # this is a liste of choosen delimiters not for sentences but for text, <H> is Hadith delimiter
class Gui_Controller(QObject):


    def __init__(self,gui:Ui_MainWindow):
        super().__init__()
        self.gui=gui
        self.INPUT_FILE = None
        self.NE_TAGS=load_ne_tag_labels()
        self.newNETags=[]



    def setup(self):
        self.gui.errorContainer.setVisible(False)
        self.gui.successContainer.setVisible(False)
        self.gui.infosGB.setVisible(False)
        self.gui.confirmButton.setVisible(False)
        #self.gui.horizontalLayout_2.setVisible(False)
        self.gui.uploadFileButton.clicked.connect(lambda: self.chooseFile())
        self.gui.startButton.clicked.connect(lambda:self.extractInformations())
        self.gui.confirmButton.clicked.connect(lambda:self.writeNewTags())


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
        self.newNETags = []
        TAGGS_TO_ADD=[]
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
                    seqtagFile.write(sentence)
                    sentence=""
                    continue
                
                trimmedLine=re.sub("\s+","",line)
                if  trimmedLine in CONTENT_DELIMITERS:
                    if not trimmedLine in contextTexts:
                        contextTexts[CONTENT_DELIMITERS[trimmedLine]]=[]
                    contextTexts[CONTENT_DELIMITERS[trimmedLine]].append(text+"\n")

                    seqtagFile.write(sentence)
                    sentence=""
                    continue

                if not re.search(r"^.+\s+.+$",line):
                    print("Input File Format Error : File is not well formated")
                    print("\t",line)
                    self.gui.errorLabel.setText("IInput File Format Error : File is not well formated, (Line "+str(totalLines)+")")
                    self.gui.errorContainer.setVisible(True)
                    return

                parts=re.split(r"\s+",line)
                sentence+=parts[1]+" "
                if parts[1].upper() in self.NE_TAGS:
                    neTagFile.write(line)
                    neTagNbr+=1
                elif parts[1].upper() == "O" or parts[1].upper() =="OTHER":
                    otherTagNbr += 1
                else:
                    self.newNETags.append(line)

                text+=parts[0]+" "

            self.gui.infosGB.setVisible(True)
            self.gui.NETagsLabel.setText(str(neTagNbr))
            self.gui.OtherTagsLabel.setText(str(otherTagNbr))
            self.gui.UnkTagsLabel.setText(str(totalLines-neTagNbr-otherTagNbr))
            

                #showing new unrecognized tags
            if len(self.newNETags)>0:
                self.gui.confirmButton.setVisible(True)
                #self.gui.horizontalLayout_2.setVisible(True)
                new_tags=[]
                for newTag in self.newNETags:
                    
                    self.gui.newWordsLabel.setText(self.gui.newWordsLabel.text()+newTag+"\n")
                    tags=[el for el in re.split("\s+",newTag)[1:] if el!=""]
                    for el in tags:

                        new_tags.append(el)

                
                new_tags=set(new_tags)    
                print(new_tags)
                if len(new_tags) >0:
                    for tag in new_tags:
                        button=QPushButton("+ "+tag)
                        button.setStyleSheet("background-color:#107ac7; color: white;")
                        button.clicked.connect(self.new_new_tag_choosed)

                        self.gui.newTagscontainer.addWidget(button)    
                    
            seqtagFile.close()
            neTagFile.close()
                # Create text corpus
            if bool(contextTexts):
                for context in contextTexts:
                    dirs=list(os.walk(BASE_CONTEXT_DIRECTORY))[0][1]
                    if context not in dirs:
                        os.mkdir(os.path.abspath(BASE_CONTEXT_DIRECTORY+"\\"+context))

                    f=open(BASE_CONTEXT_DIRECTORY+"\\"+context+"\\"+context+"_texts.txt","a",encoding="windows-1256")

                    f.writelines(contextTexts[context])    
                    f.close()


            self.gui.successContainer.setVisible(True)

        except Exception as ex:
            print("Error reading file","\n\t",str(ex))
            traceback.print_exc()
            return

    def new_new_tag_choosed(self):

        self.sender().setStyleSheet("background-color:rgb(180,180,180); color:white;")
        TAGGS_TO_ADD.append(self.sender().text().replace("+ ",""))

    def writeNewTags(self):

        base = parentdir + "\\corpus\sources\\"
        neTagFile = open(base + "emission\\" + self.INPUT_FILE[self.INPUT_FILE.rindex("/") + 1:].replace(".txt",
                                            "") + "_NELexicon.txt","a", encoding="windows-1256")
        for line in self.newNETags:
            if(re.split("\s+",line)[1] in TAGGS_TO_ADD):
                neTagFile.write(line)

        neTagFile.close()
        self.NE_TAGS=self.NE_TAGS+TAGGS_TO_ADD

        #NE_TAG_lABELS=self.NE_TAGS
        try:
            save_ne_tag_labels(self.NE_TAGS)
        except Exception as e:
            print(e)



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








