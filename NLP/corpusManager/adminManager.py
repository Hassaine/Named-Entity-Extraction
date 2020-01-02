# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 23:54:35 2020

@author: Hassaine
"""
import os,sys,inspect
import glob


position = os.path.dirname(os.path.abspath(__file__))

class corpusManager:
    def __init__(self):
        self.emissionSources=[]
        self.transitionSources=[]
    
    def loadCorpusNames(self):
        
        
        os.chdir(position.replace("\\","/")+"/../corpus/sources/emission")
        self.emissionSources =[os.path.abspath(el) for el in list(glob.glob("*.txt"))]      
        os.chdir(position)
        
        os.chdir(position.replace("\\","/")+"/../corpus/sources/transition")
        self.transitionSources =[os.path.abspath(el) for el in list(glob.glob("*.txt"))]
        os.chdir(position)
        
    
    def insert(self,wordObject,corpusName='NELexicon.txt'):
        
        word=wordObject['word']
        for tag in wordObject['tags']:
            word+=" "+tag       
        for corpus in self.emissionSources:
            if(corpus.endswith(corpusName)):
                 corpusIO = open(corpus,'a',encoding='windows-1256')
                 corpusIO.write(word)
                 corpusIO.write("\n")
                 corpusIO.close()
                 break;
                
    def update(self,wordObject,corpusName='NELexicon.txt'):
        word=wordObject['word']
        for tag in wordObject['tags']:
            word+=" "+tag    
        changed=False
        for corpus in self.emissionSources:
            if(corpus.endswith(corpusName)):
                lines = open(corpus,'r',encoding='windows-1256').readlines()
                tempFile = open('temp.txt','a',encoding='windows-1256')
                for line in lines:
                    words=line.split()
                    if(len(words)>1 and words[0]==wordObject['word']):
                        #print(word)
                        tempFile.write(word)
                        tempFile.write('\n')
                        changed=True
                        
                        
                    else:
                        tempFile.write(line)
                tempFile.close()
               
                if(changed):
                    templines = open('temp.txt','r',encoding='windows-1256').readlines()
                    updatedCorpus = open(corpus,'w',encoding='windows-1256')
                    for line in templines:
                        updatedCorpus.write(line)
                    updatedCorpus.close()
                break
        
        os.remove("temp.txt")
                        
                    
        
    def delete(self,word,corpusName='NELexicon.txt'):

        for corpus in self.emissionSources:
            if(corpus.endswith(corpusName)):
                lines = open(corpus,'r',encoding='windows-1256').readlines()
                tempFile = open('temp.txt','a',encoding='windows-1256')
                for line in lines:
                    words=line.split()
                    if(len(words)>1 and words[0]==word):
                        deleted=True
                    else:
                        tempFile.write(line)
                tempFile.close()
               
                if(deleted):
                    templines = open('temp.txt','r',encoding='windows-1256').readlines()
                    updatedCorpus = open(corpus,'w',encoding='windows-1256')
                    for line in templines:
                        updatedCorpus.write(line)
                    updatedCorpus.close()
                break
        
        os.remove("temp.txt")        
        
        
    def getEmissionSources(self):
        return [corpus[corpus.rfind('\\')+1:] for corpus in self.emissionSources]
    
    def getTransitionSources(self):
        return [corpus[corpus.rfind('\\')+1:] for corpus in self.transitionSources]
    def getCorpusJSON(self):
        pass
    
            
if __name__=='__main__':
    AM = corpusManager()
    AM.loadCorpusNames()
    #wordobj ={"word":"إدريس","tags":['PERSON']}
    #AM.insert(wordObject=wordobj)
    #AM.update(wordObject=wordobj)
    #AM.delete(word="إدريس")
    emissionList = AM.getEmissionSources()
    transitionList = AM.getTransitionSources()
#    print(AM.getEmissionSources())
#    print(AM.transitionSources())
    
       
        
        
        
    