# -*- coding: utf-8 -*-
"""
Created on Wed Dec  14 22:41:18 2019

@author: Selmane
"""
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import nltk
from nltk import defaultdict,ConditionalFreqDist
import numpy
import re
import pickle
import bases.indexes
import segtools.tokenizer
import segtools.stemer
from staticContent import *
from bases.indexes import ArabicStopWordsIndex
from segtools.tokenizer import BasicTokenize
from segtools.stemer import BasicStemmer


position = os.path.dirname(os.path.abspath(__file__))

        # ############################################ SAVE/LOAD FUNCTION
def sauvegarder_obj(obj, name:str):
    with open(os.path.join(position, name) + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def charger_obj(name:str):
    with open(os.path.join(position, name) + '.pkl', 'rb') as f:
        return pickle.load(f)


## load and save the index as JSON file   "in construction"
def loadIndexJson(index='emission.json'):
    """
    loading data methods
    """
    import simplejson as json
    with open(index, 'r', encoding='windows-1256') as f:
        return json.load(f)


## load and save the index as JSON file   "in construction"
def saveIndexjson(index, output='emission.json'):
    """
    loading data methods
    """
    import simplejson as json
    with open(output, 'w+', encoding='windows-1256') as fp:
        json.dump(index, fp, indent=' ')


## load and save the index as BINAIRE FILE
def saveIndex(index, output='emission.p'):
    """
    loading data methods
    binary file
    """
    import pickle
    with open(output, 'wb') as fp:
        pickle.dump(index, fp, protocol=pickle.HIGHEST_PROTOCOL)


def loadIndex(fileName="emission.p"):
    """
    loading data methods
    binary file
    """
    import pickle
    with open(os.path.join(position, fileName), 'rb') as fp:
        return pickle.load(fp)

    # ############################################





class Model:

    def __init__(self,stemmer=BasicStemmer()):
        self.stemmer=stemmer

    
    def saveModel(self,name:str,type="obj"):

        if type.lower()=="obj":
            sauvegarder_obj(self,name+"_Model")

    
    def train(self): pass

    
    def retrain(self): pass

    def tagText(self,text,algorithm="Viterbi"):pass

    def tagTokens(self,tokens:list,algorithm="Viterbi"):pass

    def evaluate(self,expected,results):pass


class HMM(Model):

    def __init__(self,stemmer=BasicStemmer()):
        super(HMM, self).__init__(stemmer)
        self.EMISSION_MATRIX=None
        self.TRANSITION_MATRIX = None


    def constructEmissionMatrix(self,sourceFilesList:list):
         #construction of the emission matrix
        emission = defaultdict(dict)
        for tag in NE_TAG_lABELS:
            emission[tag]=defaultdict(float)
        for fileName in sourceFilesList:
            file = open(os.path.join(position, fileName),'r',encoding='windows-1256')
            for line in file:
                words = line.split()
                entite = ''
                for word in words:
                    if(re.findall('[A-Z]+',word)==[]):
                        entite=word

                        continue

                    
                    emission[word][entite]+=1

            file.close()        


        for tag in emission.keys():
             somme=0.0
             for value in emission[tag].values():
                 somme+=value
             for word in emission[tag].keys():
                 emission[tag][word]= round(float("{0:.6f}".format(emission[tag][word]/somme)),6)

        
        self.EMISSION_MATRIX=emission
        return emission

    #saveIndex(emission1)
    #emission2 = loadIndex()

    #transision = []
    #bigrammeArray=set()

    def constructTransitionMatrix(self,sourceFilesList:list):
        #construction of the transition matrix
        transition = defaultdict(dict)
        for fileName in sourceFilesList:
            file = open(os.path.join(position, fileName),'r',encoding="windows-1256")
            fileFinal=""
            for line in file:
                line=line.upper()
                if(len(line)>1):
                    if not line.startswith("<S>"):
                        fileFinal+='<S> '+line[:-1]+' <E>\n'
                    else :
                        fileFinal+=line[:-1]+'\n'   
            file.close()             
        tokens=[el for el in re.split("[\s\n]+",fileFinal) if el!='']
        bigrams = list(nltk.bigrams(tokens))
        for (w1,w2) in bigrams:
            if w1 not in transition:
                transition[w1]=defaultdict(float)
            if w2 not in transition[w1]:
                transition[w1][w2]=0.0

            transition[w1][w2]+=1   

        for tag in transition.keys():
             somme=0.0
             for value in transition[tag].values():
                 somme+=value
             for successor in transition[tag].keys():
                 transition[tag][successor]= round(float("{0:.6f}".format(transition[tag][successor]/somme)),6)         

        
        
        self.TRANSITION_MATRIX=transition
        return transition

    
    def __viterbi(self,observations:list,emissionTable:ConditionalFreqDist,transitionTable:dict):
        N=len(transitionTable)
        T=len(observations)
        viterbi=numpy.ndarray(shape=( N+2,T ) )
        tags=[el for el in list(emissionTable)]
        backTrack=[]


        for i in range(N):
            viterbi[i,0]=emissionTable[observations[0]][tags[i]]*(emissionTable["<S>"][tags[i]] if tags[i] in emissionTable["<S>"] else 0.0)

        for oIndex in range(1,T):
            for tIndex in range(N):
                bestTagIndex=numpy.argmax([viterbi[i,oIndex-1] for i  in range(N)])
                bestTag=tags[bestTagIndex]
                backTrack.append((observations[oIndex-1],bestTag))
                viterbi[tIndex,oIndex]=viterbi[bestTagIndex,oIndex-1]*\
                                       emissionTable[observations[oIndex]][tags[i]]*\
                                       (emissionTable[bestTag][tags[i]] if tags[i] in emissionTable[bestTag] else 0.0)
        



        return backTrack


        ################################OVVERRIDES################################

    def train(self): pass

    
    def retrain(self): pass

    def tagText(self,text,algorithm="Viterbi"):
        Tokenizer=BasicTokenize()
        tokens=Tokenizer.tokenize(text)
        print(tokens)
        return self.__viterbi(tokens, self.EMISSION_MATRIX, self.TRANSITION_MATRIX)

    def tagTokens(self,tokens:list,algorithm="Viterbi"):
        return self.__viterbi(tokens,self.EMISSION_MATRIX,self.TRANSITION_MATRIX)


    def evaluate(self,expected,results):pass


if __name__=='__main__':
    fileName="corpus/samples/input.txt"
    HmmModel=HMM()
    HmmModel.constructTransitionMatrix(["../corpus/sources/transition/NEtagSeq.txt"])
    HmmModel.constructEmissionMatrix(["../corpus/sources/emission/NELexicon.txt"])
    #print(HmmModel.tagText(open(fileName,"r",encoding="windows-1256").read()))







    
        
    
 