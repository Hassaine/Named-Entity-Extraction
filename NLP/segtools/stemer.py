import nltk
import tokenizer
from nltk import stem
from nltk.stem.arlstem import ARLSTem
from nltk.stem.isri import ISRIStemmer
from tokenizer import *
from nltk.stem import WordNetLemmatizer
import re
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(currentdir+"\\bases")
from indexes import ArabicStopWordsIndex

class Stemmer:
    
    def getStems(self,tokens,flag=False): pass

    
    def normalize(self,word): pass




class BasicStemmer(Stemmer):

    def __init__(self):
        self.stemmer = ISRIStemmer()

    def getStems(self,tokens,flag=False):

        rootList=[]

        for token in tokens:
            #token=stemmer.norm(token)
            root=self.stemmer.pre32(token)
            rootList.append(root)
            print(token,"  :  ",root)

        return rootList



    def loadStemsDictionnary(self,filePath="dictStems.txt"):
        lines=open(filePath,"r",encoding="windows-1256").readlines()
        dictionary=nltk.defaultdict(list)
        for line in lines:
            if not re.match("^;.*",line):
                parts=line.split('\t')
                if len(parts)!=4:
                    break
                else:
                    [rootStem,stem,tag,enGloss]=parts
                    dictionary[rootStem].append([stem,tag,' '.join(enGloss.split(';'))])

        return dictionary


    def verify(self,word):
        if self.stopWordsIndex.access(word):
            return True

    def setStopWordsIndex(self,index:ArabicStopWordsIndex):
        self.stopWordsIndex=index





