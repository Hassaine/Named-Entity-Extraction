import nltk
from nltk import stem
from nltk.stem.arlstem import ARLSTem
from nltk.stem.isri import ISRIStemmer
from tokenizer import *
from nltk.stem import WordNetLemmatizer
from indexes import *
from traitements import *
import re

class Stemmer:
    @classmethod
    def getStems(self,tokens,flag=False): pass

    @classmethod
    def normalize(self,word): pass




class BasicStemmer(Stemmer):

    def __init__(self):
        self.stemmer = ISRIStemmer()

    def getStems(self,tokens,flag=False):

        rootList=[]

        for token in tokens:
            #token=stemmer.norm(token)
            root=self.stemmer.stem(token)
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
        if ARABIC_STOPWORDS_INDEX.access(word):
            return True


'''
tokens=tokenize("input.txt")
print("Tokenization result : ",str(tokens))

getstem(tokens)
BasicStemmer().loadStemsDictionnary()
'''



