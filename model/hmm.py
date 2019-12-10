# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 10:41:18 2019

@author: Hassaine
"""

import nltk
from nltk import defaultdict
import re
import pickle
import os



        # ############################################ SAVE/LOAD FUNCTION
def sauvegarder_obj(obj, name:str):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def charger_obj(name:str):
    with open(name + '.pkl', 'rb') as f:
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
    with open(fileName, 'rb') as fp:
        return pickle.load(fp)

    # ############################################





class Model:

    def __init__(self,stemmer):
        self.stemmer=stemmer

    @classmethod
    def saveModel(self,name:str,type="obj"):

        if type.lower()=="obj":
            sauvegarder_obj(self,name+"_Model")

    @classmethod
    def train(self): pass

    @classmethod
    def retrain(self): pass


class HMM(Model):



    def constructEmissionMatrix(self,sourceFilesList:list):
         #construction of the emission matrix
        emission = defaultdict(float)
        for tag in ['PERSON','ORG','OTHER','LOC','DATE','OCLUE','DCLUE','LCLUE','PCLUE','PREP','PUNC','CONJ','NPREFIX','DEF']:
            emission[tag]={}
        for fileName in sourceFilesList:
            file = open(fileName,'r',encoding='windows-1256')
            for line in file:
                words = line.split()
                entite = ''
                for word in words:
                    if(re.findall('[A-Z]+',word)==[]):
                        entite=word

                        continue

                    if( emission[word].get(entite,None) is None):
                        emission[word][entite]=1
                    else:
                        emission[word][entite]+=1


        for tag in emission.keys():
             somme=0.0
             for value in emission[tag].values():
                 somme+=value
             for word in emission[tag].keys():
                 emission[tag][word]= round(float("{0:.6f}".format(emission[tag][word]/somme)),6)


        return emission

    #saveIndex(emission1)
    #emission2 = loadIndex()

    #transision = []
    #bigrammeArray=set()

    def constructTransitionMatrix(self,sourceFilesList:list):
        #construction of the transition matrix

        for fileName in sourceFilesList:
            file = open(fileName,'r',encoding="windows-1256")
            fileFinal=""
            for line in file:
                if(len(line)>1):
                    fileFinal+='<S> '+line[:-1]+' <E>\n'


        bigrams = nltk.bigrams(fileFinal.split())


        cfd = nltk.ConditionalFreqDist(bigrams)
        cfd.tabulate()


HMM(None).constructTransitionMatrix(["NEtagSeq.txt"])







    
        
    
 