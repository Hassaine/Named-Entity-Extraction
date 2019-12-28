# -*- coding: utf-8 -*-
"""
Created on Wed Dec  14 22:41:18 2019

@author: Selmane
"""
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
sys.path.append(parentdir+"\\segtools")
sys.path.append(parentdir+"\\bases")
sys.path.append(parentdir+"\\statics")
import nltk
from nltk import defaultdict,ConditionalFreqDist
from nltk import bigrams,trigrams,ngrams
import numpy
import re

    #user modules

import pickle
import tokenizer
import stemer
import indexes
import staticMethods
from staticMethods import *
from staticContent import *
from indexes import ArabicStopWordsIndex
from tokenizer import BasicTokenize
from stemer import BasicStemmer


position = os.path.dirname(os.path.abspath(__file__))

staticMethods.position=position



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

    def loadTables(self):


        if not bool(self.EMISSION_MATRIX):
            if not os.path.exists('obj/hmm/emissionTable.json'):
                print("Emission table not found in Disk, reconstructing and saving ....")
                import glob
                print(position)
                os.chdir(position.replace("\\","/")+"/../corpus/sources/emission")
                emissionSources =[os.path.abspath(el) for el in list(glob.glob("*.txt")) ]

                os.chdir(position)
                self.EMISSION_MATRIX = self.constructEmissionMatrix(emissionSources)
                saveIndex(self.EMISSION_MATRIX,"obj\\hmm\\emissionTable.pkl")
                saveIndexjson(self.EMISSION_MATRIX, "obj\\hmm\\emissionTable.json")
            else:
                self.EMISSION_MATRIX=loadIndexJson("obj/hmm/emissionTable.json")
                print("Emission table loaded from Disk ...")

        if not bool(self.TRANSITION_MATRIX):
            if not os.path.exists('obj/hmm/transitionTable.json'):
                print("Transition table not found in Disk, reconstructing and saving ....")
                import glob
                os.chdir("../corpus/sources/transition")
                transitionSources =[os.path.abspath(el) for el in list(glob.glob("*.txt")) ]
                os.chdir(position)
                self.TRANSITION_MATRIX = self.constructTransitionMatrix(transitionSources)
                saveIndex(self.TRANSITION_MATRIX,"obj\\hmm\\transitionTable.pkl")
                saveIndexjson(self.TRANSITION_MATRIX, "obj\\hmm\\transitionTable.json")
            else:
                self.TRANSITION_MATRIX=loadIndexJson("obj/hmm/transitionTable.json")
                print("Transition table loaded from Disk ...")




    def constructEmissionMatrix(self,sourceFilesList:list):
         #construction of the emission matrix
        emission = defaultdict(dict)
        for tag in NE_TAG_lABELS:
            emission[tag]=defaultdict(float)
        for fileName in sourceFilesList:
            file = open(fileName,'r',encoding='windows-1256')
            for line in file:
                words = re.split("\s+",line)
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
            file = open(fileName,'r',encoding="windows-1256")
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
        Bigrams = list(nltk.bigrams(tokens))
        for (w1,w2) in Bigrams:
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

    
    def __viterbi(self,observations:list,emissionTable:dict,transitionTable:dict):
        N=len(transitionTable)
        
        T=len(observations)
        viterbi=numpy.zeros(( N+2,T ) )
        
        
        # the intialProba is independent of the transition proba
        initialProbability = transitionTable["<S>"]
      
        tags=[el for el in list(transitionTable.keys())]
        
        #we remove the <S> from TAGS  because its just a sign of sentence start
        tags.remove('<S>')
        N-=1
		 
		
		
        backTrack=[]

        for i in range(N):
            if tags[i]!="<S>" and tags[i]!="<E>":
                if tags[i] not in emissionTable:
                    emissionTable[tags[i]]=defaultdict(float)
                viterbi[i,0]=round(float("{0:.6f}".format((emissionTable[tags[i]][observations[0]] if observations[0] in emissionTable[tags[i]] else  0.0)*(initialProbability[tags[i]] if tags[i] in initialProbability else 0.0))),6)

        
        
        
		
		
        for oIndex in range(1,T):
            bestTagIndex=numpy.argmax([viterbi[i,oIndex-1] for i  in range(N)])
            bestTag=tags[bestTagIndex]
            backTrack.append((observations[oIndex-1],bestTag))   
            for tIndex in range(N):
                if tags[tIndex]=='<E>':continue
                
                viterbi[tIndex,oIndex]=viterbi[bestTagIndex,oIndex-1]*\
                                       (emissionTable[tags[tIndex]][observations[oIndex]] if observations[oIndex] in emissionTable[tags[tIndex]] else 0.0)*\
                                       (transitionTable[bestTag][tags[tIndex]] if tags[tIndex] in transitionTable[bestTag] else 0.0)


                #if the observation belong to another TAG then OTHER we eliminate OTHER ps: the index of the tag OTHER on TAGS array is 0
                if(tIndex>0 and  viterbi[tIndex,oIndex]>0.0 ) :
                    viterbi[0,oIndex]=0.0;
					
					
        #we save the backtrack of the last Observation
        bestTagIndex=numpy.argmax([viterbi[i,T-1] for i  in range(N)])
        bestTag=tags[bestTagIndex]
        backTrack.append((observations[T-1],bestTag)) 
        
        return backTrack


        ################################OVVERRIDES################################

    def train(self): pass

    
    def retrain(self): pass

    def tagText(self,text,algorithm="Viterbi"):
        self.loadTables()

        Tokenizer=BasicTokenize()
        tokens=Tokenizer.tokenize(text)

        return self.__viterbi(tokens, self.EMISSION_MATRIX, self.TRANSITION_MATRIX)

    def tagTokens(self,tokens:list,algorithm="Viterbi"):
        self.loadTables()
        return self.__viterbi(tokens,self.EMISSION_MATRIX,self.TRANSITION_MATRIX)


    def evaluate(self,expected,results):pass


class TrigramHMM(HMM):

    def __init__(self, stemmer=BasicStemmer()):
        super(TrigramHMM, self).__init__(stemmer)
        self.EMISSION_MATRIX = None
        self.TRANSITION_MATRIX = None


    def constructEmissionMatrix(self, sourceFilesList: list):
        # construction of the emission matrix
        emission = defaultdict(dict)
        for tag in NE_TAG_lABELS:
            emission[tag] = defaultdict(float)
        for fileName in sourceFilesList:
            file = open(fileName, 'r', encoding='windows-1256')
            for line in file:
                words = re.split("\s+", line)
                entite = ''
                for word in words:
                    if (re.findall('[A-Z]+', word) == []):
                        entite = word

                        continue

                    emission[word][entite] += 1

            file.close()

        for tag in emission.keys():
            somme = 0.0
            for value in emission[tag].values():
                somme += value
            for word in emission[tag].keys():
                emission[tag][word] = round(float("{0:.6f}".format(emission[tag][word] / somme)), 6)

        self.EMISSION_MATRIX = emission
        return emission

    def constructTransitionMatrix(self,sourceFilesList:list):
        #construction of the transition matrix
        transition={}
        for fileName in sourceFilesList:
            file = open(fileName,'r',encoding="windows-1256")
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
        Trigrams = list(trigrams(tokens))
        for (w1,w2) in Trigrams:
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

    def __viterbi(self, observations: list, emissionTable: dict, transitionTable: dict):
        N = len(transitionTable)

        T = len(observations)
        viterbi = numpy.zeros((N + 2, T))

        # the intialProba is independent of the transition proba
        initialProbability = transitionTable["<S>"]

        tags = [el for el in list(transitionTable.keys())]

        # we remove the <S> from TAGS  because its just a sign of sentence start
        tags.remove('<S>')
        N -= 1

        backTrack = []

        for i in range(N):
            if tags[i] != "<S>" and tags[i] != "<E>":
                if tags[i] not in emissionTable:
                    emissionTable[tags[i]] = defaultdict(float)
                viterbi[i, 0] = round(float("{0:.6f}".format(
                    (emissionTable[tags[i]][observations[0]] if observations[0] in emissionTable[tags[i]] else 0.0) * (
                        initialProbability[tags[i]] if tags[i] in initialProbability else 0.0))), 6)

        for oIndex in range(1, T):
            bestTagIndex = numpy.argmax([viterbi[i, oIndex - 1] for i in range(N)])
            bestTag = tags[bestTagIndex]
            backTrack.append((observations[oIndex - 1], bestTag))
            for tIndex in range(N):
                if tags[tIndex] == '<E>': continue

                viterbi[tIndex, oIndex] = viterbi[bestTagIndex, oIndex - 1] * \
                                          (emissionTable[tags[tIndex]][observations[oIndex]] if observations[oIndex] in
                                                                                                emissionTable[tags[
                                                                                                    tIndex]] else 0.0) * \
                                          (transitionTable[bestTag][tags[tIndex]] if tags[tIndex] in transitionTable[
                                              bestTag] else 0.0)

                # if the observation belong to another TAG then OTHER we eliminate OTHER ps: the index of the tag OTHER on TAGS array is 0
                if (tIndex > 0 and viterbi[tIndex, oIndex] > 0.0):
                    viterbi[0, oIndex] = 0.0;

        # we save the backtrack of the last Observation
        bestTagIndex = numpy.argmax([viterbi[i, T - 1] for i in range(N)])
        bestTag = tags[bestTagIndex]
        backTrack.append((observations[T - 1], bestTag))

        return backTrack
        
    def evaluate(self, expected, results):
        pass


if __name__=='__main__':
    fileName="../corpus/samples/input.txt"
    HmmModel=HMM()
    #HmmModel.constructTransitionMatrix(["../corpus/sources/transition/NEtagSeq.txt"])
    #HmmModel.constructEmissionMatrix(["../corpus/sources/emission/NELexicon.txt"])
    print(HmmModel.tagText(open(fileName,"r",encoding="windows-1256").read())[:200])








    
        
    
 