# -*- coding: utf-8 -*-
"""
Created on Wed Dec  14 22:41:18 2019

@author: Selmane
"""

import os,sys,inspect
from ast import literal_eval as tuple_parser
import nltk
from nltk import defaultdict,ConditionalFreqDist,FreqDist,pprint
from nltk import bigrams,trigrams,ngrams
import numpy,re,random
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
sys.path.append(parentdir+"\\segtools")
sys.path.append(parentdir+"\\bases")
sys.path.append(parentdir+"\\statics")

    #user modules

import staticMethods
from staticMethods import *
import staticContent
from staticContent import *
from tokenizer import BasicTokenize
from stemer import BasicStemmer

global NE_TAG_lABELS

position = os.path.dirname(os.path.abspath(__file__))

staticMethods.position=position



class Model:

    def __init__(self,stemmer=BasicStemmer(),backoff=None):
        self.stemmer=stemmer
        self.bacckoff=backoff

    
    def saveModel(self,name:str,type="obj"):

        if type.lower()=="obj":
            sauvegarder_obj(self,name+"_Model")

    
    def train(self,tagged_corpus): pass

    
    def retrain(self): pass

    def tagText(self,text,algorithm="Viterbi"):pass

    def tagTokens(self,tokens:list,algorithm="Viterbi"):pass

    def backOffPrent(self,backTrack:list): pass

    def evaluate(self,expected,results):pass




class UnigramHMM(Model):

    def __init__(self,table, stemmer=BasicStemmer(), backoff: Model = None):
        super(UnigramHMM, self).__init__(stemmer, backoff)
        self.table=table

    def tagword(self,word):
        if self.table is not None:
            if word in self.table:
                return max([self.table[word][el] for el in list(self.table[word])])
        if re.match("[٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩]+", word) or re.match("[0-9]+", word):
            return "NUMBER"
        if len(word) <= 2:
            return "PREP"

        return "OTHER"


    def tagText(self, text, algorithm="Viterbi"):
        Tokenizer = BasicTokenize()
        tokens = Tokenizer.tokenize(text)
        tokens = [self.stemmer.stem(token) for token in tokens]
        return self.tagTokens(tokens)

    def tagTokens(self, tokens: list, algorithm="Viterbi"):

        if self.table is None:
            self.table
        tokens = [self.stemmer.stem(token) for token in tokens]
        for token in tokens:

            root=self.stemmer.stem(token)
            if token in self.table:
                return max([self.table[token][el] for el in list(self.table[token])])
            elif root in self.table:
                return max([self.table[root][el] for el in list(self.table[root])])

            if re.match("[٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩]+",root):
                return "NUMBER"
            if len(token)<=2 or len(root)<=2:

                return "PREP"

            return "OTHER"


class HMM(Model):

    def __init__(self,stemmer=BasicStemmer(),backoff:UnigramHMM=None):
        super(HMM, self).__init__(stemmer,backoff)
        self.EMISSION_MATRIX=None
        self.TRANSITION_MATRIX = None
        self.transMatrix_file_save_name="transitionTable"
        self.emissMatrix_file_save_name = "emissionTable"
        NE_TAG_lABELS=load_ne_tag_labels()
        self.ne_set=None
        self.tag_set=None

    def loadTables(self):

        if not bool(self.EMISSION_MATRIX):
            if not os.path.exists(position+'/obj/hmm/emissionTable.json'):
                print("Emission table not found in Disk, reconstructing and saving ....")
                import glob
                print(position)
                os.chdir(position.replace("\\", "/") + "/../corpus/sources/emission")
                emissionSources = [os.path.abspath(el) for el in list(glob.glob("*.txt"))]

                os.chdir(position)
                self.EMISSION_MATRIX = self.constructEmissionMatrix(emissionSources)
                saveIndex(self.EMISSION_MATRIX, "obj\\hmm\\emissionTable.pkl")
                saveIndexjson(self.EMISSION_MATRIX, "obj\\hmm\\emissionTable.json")
            else:
                self.EMISSION_MATRIX = loadIndexJson(position+"/obj/hmm/emissionTable.json")
                print("Emission table loaded from Disk ...")

        if not bool(self.TRANSITION_MATRIX):
            if not os.path.exists(position+'/obj/hmm/transitionTable.json'):
                print("Transition table not found in Disk, reconstructing and saving ....")
                import glob
                os.chdir("../corpus/sources/transition")
                transitionSources = [os.path.abspath(el) for el in list(glob.glob("*.txt"))]
                os.chdir(position)
                self.TRANSITION_MATRIX = self.constructTransitionMatrix(transitionSources)
                saveIndex(self.TRANSITION_MATRIX, "obj\\hmm\\transitionTable.pkl")
                saveIndexjson(self.TRANSITION_MATRIX, "obj\\hmm\\transitionTable.json")
            else:
                self.TRANSITION_MATRIX = loadIndexJson(position+"/obj/hmm/transitionTable.json")
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
                    word=self.stemmer.stem(word)
                    if(re.findall('[A-Z]+',word)==[]):
                        entite=word

                        continue
                    if word not in emission:
                        emission[word] = defaultdict(float)

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


    def buildEmissionMatrix(self,taggedCorpus:list,train_size):
        train=taggedCorpus[:int(train_size*len(taggedCorpus))]
        random.shuffle(train)
         #construction of the emission matrix
        emission = defaultdict(dict)
        for tag in self.ne_set:
            emission[tag.upper()]=defaultdict(float)
        for tuple in train:
            word = self.stemmer.stem(tuple[0])
            emission[tuple[1].upper()][word]+=1
                    

        for tag in emission.keys():
             somme=0.0
             for value in emission[tag].values():
                 somme+=value
             for word in emission[tag].keys():
                 emission[tag][word]= round(float("{0:.6f}".format(emission[tag][word]/somme)),6)

        
        self.EMISSION_MATRIX=emission
        return emission

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


    def buildTransitionMatrix(self,tagged_corpus:list,train_size):
        train=tagged_corpus[:int(train_size*len(tagged_corpus))]
        random.shuffle(train)
            #construction of the transition matrix
        transition = ConditionalFreqDist()
        for (tag1,tag2) in train:
            
            if tag1 not in transition:
                transition[tag1]=FreqDist()
            if tag2 not in transition[tag1]:
                transition[tag1][tag2]=0.0

            transition[tag1][tag2]+=1   

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
      
        tags=[el for el in list(emissionTable.keys())]
        
            #we remove the <S> from TAGS  because its just a sign of sentence start
        #tags.remove('<S>')
        N-=1
		 
		
		
        backTrack=[]
        for i in range(N):

                if tags[i] not in emissionTable:
                    print("not found")
                    emissionTable[tags[i]]=defaultdict(float)
                print(observations[0],tags[i],observations[0] in emissionTable[tags[i]])
                viterbi[i,0]=round(float("{0:.6f}".format((emissionTable[tags[i]][observations[0]] if observations[0] in emissionTable[tags[i]] else  0.0)*(initialProbability[tags[i]] if tags[i] in initialProbability else 0.0))),6)

        
        

		
		
        for oIndex in range(1,T):
            print([viterbi[i,oIndex-1] for i  in range(N)])
            bestTagIndex=numpy.argmax([viterbi[i,oIndex-1] for i  in range(N)])
            bestTag=tags[bestTagIndex]
            print("Last word was tagged as ",observations[oIndex-1]," ",bestTag)
            backTrack.append((observations[oIndex-1],bestTag))   
            for tIndex in range(N):
                #if tags[tIndex]=='<E>':continue
                
                viterbi[tIndex,oIndex]=viterbi[bestTagIndex,oIndex-1]*\
                                       (emissionTable[tags[tIndex]][observations[oIndex]] if observations[oIndex] in emissionTable[tags[tIndex]] else 0.0)*\
                                       (transitionTable[bestTag][tags[tIndex]] if tags[tIndex] in transitionTable[bestTag] else 0.0)


                    #if the observation belong to another TAG then OTHER we eliminate OTHER ps: the index of the tag OTHER on TAGS array is 0
                # if(tIndex>0 and  viterbi[tIndex,oIndex]>0.0 ) :
                #     viterbi[0,oIndex]=0.0
					
					
            #we save the backtrack of the last Observation
        bestTagIndex=numpy.argmax([viterbi[i,T-1] for i  in range(N)])
        bestTag=tags[bestTagIndex]
        backTrack.append((observations[T-1],bestTag)) 
        
        return backTrack


        ################################OVVERRIDES################################

    def train(self,tagged_corpus,test_size=0.2):
        self.ne_set=[el[1] for el in tagged_corpus ]
        self.tag_set=list(bigrams([el[1] for el in tagged_corpus]))

        self.buildEmissionMatrix(tagged_corpus,1-test_size)
        self.buildTransitionMatrix(tagged_corpus,1-test_size)




    
    def retrain(self):
        if self.ne_set is not None and self.tag_set is not None:
            self.constructEmissionMatrix(self.ne_set,0)
            self.constructTransitionMatrix(self.tag_set,0)

    def tagText(self,text,algorithm="Viterbi"):
        self.loadTables()

        Tokenizer=BasicTokenize()
        tokens=Tokenizer.tokenize(text)
        tokens=[self.stemmer.stem(token) for token in tokens]

        return self.__viterbi(tokens, self.EMISSION_MATRIX, self.TRANSITION_MATRIX)

    def tagTokens(self,tokens:list,algorithm="Viterbi"):
        self.loadTables()
        tokens = [self.stemmer.stem(token) for token in tokens]
        return self.__viterbi(tokens,self.EMISSION_MATRIX,self.TRANSITION_MATRIX)


    def evaluate(self,expected,results):
        precision=recall=f_measure=0.0

        expected=[(self.stemmer.stem(el[0]),el[1]) for el in expected]
        gold_size=len(expected)
        result_size=len(results)
        for i in range(len(results)):

            if results[i]in expected:
                precision+=1/result_size
                recall+=1/gold_size

        if precision+recall!=0:
            f_measure=precision*recall/(precision+recall)
        else:
            f_measure=0

        return (precision,recall,f_measure)


class TrigramHMM(HMM):

    def __init__(self, stemmer=BasicStemmer(),backoff:Model=None):
        super(TrigramHMM, self).__init__(stemmer,backoff)
        self.EMISSION_MATRIX = None
        self.TRANSITION_MATRIX = None
        self.transMatrix_file_save_name="trigram_transitionTable"
        self.emissMatrix_file_save_name="trigram_emissionTable"


    def loadTables(self):


        if not bool(self.EMISSION_MATRIX):
            if not os.path.exists('obj/hmm/'+self.emissMatrix_file_save_name+'.json'):
                print("Emission table not found in Disk, reconstructing and saving ....")
                import glob

                os.chdir(position.replace("\\","/")+"/../corpus/sources/emission")
                emissionSources =[os.path.abspath(el) for el in list(glob.glob("*.txt")) ]

                os.chdir(position)
                self.EMISSION_MATRIX = self.constructEmissionMatrix(emissionSources)
                saveIndex(self.EMISSION_MATRIX,"obj\\hmm\\"+self.emissMatrix_file_save_name+'.pkl')
                saveIndexjson(self.EMISSION_MATRIX, "obj\\hmm\\"+self.emissMatrix_file_save_name+'.json')
            else:
                self.EMISSION_MATRIX=loadIndexJson("obj/hmm/"+self.emissMatrix_file_save_name+'.json')
                #self.EMISSION_MATRIX = loadIndex("obj/hmm/" + self.emissMatrix_file_save_name + '.pkl')
                print("Emission table loaded from Disk ...")

        if not bool(self.TRANSITION_MATRIX):
            if not os.path.exists(position+'/obj/hmm/'+self.transMatrix_file_save_name+'.pkl'):
                print("Transition table not found in Disk, reconstructing and saving ....")
                import glob
                os.chdir("../corpus/sources/transition")
                transitionSources =[os.path.abspath(el) for el in list(glob.glob("*.txt")) ]
                os.chdir(position)
                self.TRANSITION_MATRIX = self.constructTransitionMatrix(transitionSources)
                #saveIndex(self.TRANSITION_MATRIX,"obj\\hmm\\"+self.transMatrix_file_save_name+'.pkl')
                save_obj(self.TRANSITION_MATRIX, "obj\\hmm\\"+self.transMatrix_file_save_name+'.pkl')
            else:
                self.TRANSITION_MATRIX=load_obj("obj/hmm/"+self.transMatrix_file_save_name+'.pkl')
                try:


                    convertedCond = [tuple_parser(cond) for cond in self.TRANSITION_MATRIX.conditions()]
                    cfd=ConditionalFreqDist([(tuple_parser(cond),tag) for cond in self.TRANSITION_MATRIX.conditions() for tag in self.TRANSITION_MATRIX[cond] ])

                    self.TRANSITION_MATRIX=cfd
                except Exception as e:
                    print(e)
                print("Transition table loaded from Disk ...", end=" ")


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
                    word=self.stemmer.stem(word)
                    if (re.findall('[A-Z]+', word) == []):
                        entite = word

                        continue
                    if not word in emission:
                        emission[word] = defaultdict(float)

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
        self.initialProbabilities=FreqDist([tokens[i] for i in range(1,len(tokens)) if tokens[i-1]=='<S>'])

        self.tags=list(set(tokens))
        self.bigramDist=FreqDist(list(bigrams(tokens)))
        Trigrams = list(trigrams(tokens))
        cfd=ConditionalFreqDist(((el[2],(el[0],el[1])) for el in Trigrams))

        for word in cfd.conditions():
            for bigram in cfd[word]:
                cfd[word][bigram]=round(float("{0:.6f}".format(cfd[word].freq(bigram))),6)


        

        self.TRANSITION_MATRIX=cfd
        return cfd

    def __viterbi(self, observations: list, emissionTable: dict, transitionTable: ConditionalFreqDist):


        if not hasattr(self,'bigramDist'):
            listcouples=[]
            for tag in self.TRANSITION_MATRIX.conditions():
                for bigram in self.TRANSITION_MATRIX[tag]:
                    listcouples.append(bigram)
                    if not hasattr(self, 'tags'):
                        self.tags = []
                    if not bigram[0] in self.tags: self.tags.append(bigram[0])
                    if not bigram[1] in self.tags: self.tags.append(bigram[1])
            self.bigramDist=FreqDist(listcouples)
            for  key in self.bigramDist:
                self.bigramDist[key]=self.bigramDist[key]/self.bigramDist.N()  # or simply self.bigramDist.freq(key)
            print("no bigramDist.... Creating bigramDist")

        if not hasattr(self, 'initialProbabilities'):
            print("no inital distribution.... Creating initDist")
            self.initialProbabilities=FreqDist(el[1] for el in self.bigramDist if el[0]=='<S>')
            for tag in self.initialProbabilities:
                    self.initialProbabilities[tag]=self.initialProbabilities[tag]/self.initialProbabilities.N()

        N = len(self.tags)

        T = len(observations)
        viterbi = numpy.zeros((N + 2, T))






        # we remove the <S> from TAGS  because its just a sign of sentence start
        if "<S>" in self.tags:
            self.tags.remove('<S>')
            N -= 1

        backTrack = []

        for i in range(N):


                if self.tags[i] not in emissionTable:
                    emissionTable[self.tags[i]] = defaultdict(float)
                viterbi[i, 0] = round(float("{0:.6f}".format(
                    (emissionTable[self.tags[i]][observations[0]] if observations[0] in emissionTable[self.tags[i]] else 0.0) * (
                        self.initialProbabilities[self.tags[i]] if self.tags[i] in self.initialProbabilities else 0.0))), 6)

        for oIndex in range(1, T):
            bestTagIndex = numpy.argmax([viterbi[i, oIndex - 1] for i in range(N)])
            bestTag = self.tags[bestTagIndex]
            bestTag2 = self.tags[numpy.argmax([viterbi[i, oIndex - 2] for i in range(N)])] if oIndex != 1 else "<S>"
            if viterbi[bestTagIndex, oIndex-1] == 0:
                print("Zero resulting probability. Couldn't tag ",observations[oIndex-1],"Previous besttag was :",bestTag2, end=" ")
                if self.bacckoff is not None:
                    self.bacckoff.loadTables()
                    best=None
                    max=0
                    for tag in self.bacckoff.TRANSITION_MATRIX[bestTag2]:

                        if self.bacckoff.TRANSITION_MATRIX[bestTag2][tag]>max:

                            max=self.bacckoff.TRANSITION_MATRIX[bestTag2][tag]
                            best=tag
                            print("Best tag so fat ",best, end=" ")
                    if best is not None:
                        viterbi[bestTagIndex, oIndex - 1]=max*self.EMISSION_MATRIX[best][observations[oIndex-1]] if observations[oIndex-1] in self.EMISSION_MATRIX[best] else 0.0
                        bestTag=self.tags[bestTagIndex]#viterbi[bestTagIndex, oIndex - 1]

                    if viterbi[bestTagIndex, oIndex - 1]==0:
                        if self.bacckoff.bacckoff is not None:
                            self.bacckoff.bacckoff.tagword(observations[0])

                        else:
                            viterbi[bestTagIndex, oIndex - 1]=1
                            bestTag="OTHER"

                else:
                    viterbi[bestTagIndex, oIndex - 1] = 1
                    bestTag = "OTHER"
                print(" Backoff tag : ",bestTag, "viterbi : ",viterbi[bestTagIndex, oIndex - 1])
            #print([viterbi[i, oIndex-1] for i in range(N) ])
            backTrack.append((observations[oIndex - 1], bestTag))
            for tIndex in range(N):
                if self.tags[tIndex] == '<E>': continue

                viterbi[tIndex, oIndex] = viterbi[bestTagIndex, oIndex - 1] * \
                                          (emissionTable[self.tags[tIndex]][observations[oIndex]] if observations[oIndex] in
                                                                                                emissionTable[self.tags[
                                                                                                    tIndex]] else 0.0) * \
                                          (transitionTable[self.tags[tIndex]][(bestTag,bestTag2)] if (bestTag,bestTag2) in transitionTable[self.tags[tIndex]] else 0.0)

                # if the observation belong to another TAG then OTHER we eliminate OTHER ps: the index of the tag OTHER on TAGS array is 0
                '''if (tIndex > 0 and viterbi[tIndex, oIndex] > 0.0):
                    viterbi[0, oIndex] = 0.0;'''







        # we save the backtrack of the last Observation
        bestTagIndex = numpy.argmax([viterbi[i, T - 1] for i in range(N)])
        bestTag = self.tags[bestTagIndex]
        backTrack.append((observations[T - 1], bestTag))

        for (word,tag) in backTrack:
            if tag=='UNKNWN':
                if self.bacckoff is None:
                    tag="OTHER"
                else:
                    self.bacckoff.backOffPrent(backTrack)

        return backTrack

    def tagText(self,text,algorithm="Viterbi"):
        self.loadTables()

        Tokenizer=BasicTokenize()
        tokens=Tokenizer.tokenize(text)
        tokens = [self.stemmer.stem(token) for token in tokens]
        return self.__viterbi(tokens, self.EMISSION_MATRIX, self.TRANSITION_MATRIX)

    def tagTokens(self,tokens:list,algorithm="Viterbi"):
        self.loadTables()
        tokens = [self.stemmer.stem(token) for token in tokens]
        return self.__viterbi(tokens,self.EMISSION_MATRIX,self.TRANSITION_MATRIX)





def save_results(file_name,allresults):
    import pandas as pd

    writer = pd.ExcelWriter(
        file_name, engine='xlsxwriter')

    df = pd.DataFrame()
    sumR = maxR = 0
    sumP = maxP = 0
    sumF = maxF = 0
    for tuple in allresults:

        sumR += tuple[1][1]
        sumP += tuple[1][0]
        sumF += tuple[1][2]
        if tuple[1][1] > maxR:
            maxR = tuple[1][1]
        if tuple[1][0] > maxP:
            maxP = tuple[1][0]
        if tuple[1][2] > maxF:
            maxF = tuple[1][2]
        df = df.append(pd.DataFrame({'Text': [tuple[0]],
                                     'Recall': [tuple[1][1]],
                                     'Precision': [tuple[1][0]],
                                     'F_measure': [tuple[1][2]]}), ignore_index=True)

    df = df.append(pd.DataFrame({
                                     'Best_Recall': [maxR],
                                     'Best_Precision': [maxP],
                                     'Best_F_measure': [maxP],
                                     'Average_Recall': [sumR / len(allresults)],
                                     'Average_Precision': sumP / len(allresults),
                                     'Average_F_measure': sumF / len(allresults)}), ignore_index=True)

    df.to_excel(writer, sheet_name='Results', startrow=1, header=False)

    workbook = writer.book
    worksheet = writer.sheets['Results']
    header_format = workbook.add_format({'bold': True,
                                         'bottom': 2,
                                         'bg_color': '#4e8ef5'})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num + 1, value, header_format)

    writer.save()



            ###############################################################################"
def test_sentences_tag(tagger:Model,file_name="../corpus/samples/saieinput_sample.txt"):
    sentences=open(file_name, "r", encoding="windows-1256").readlines()

    for sentence in sentences:
        print("Tagging sentence : <<",sentence," >>")
        tagged=tagger.tagText(sentence)
        for el in tagged:print(el[0]+"/"+el[1],end="  ")
        print("\n")
def evaluation(tagger,sentences):

        expected=[]
        text=""
        i=0
        all_results=[]
        for line in sentences:
            line=line.upper()
            if i>50:break
            if line.startswith("<H>") or line.startswith("***") :
                tagged = tagger.tagText(text)
                print("expected ", expected)
                print("returned", tagged)
                eval=tagger.evaluate(expected, tagged)
                all_results.append((text,eval))
                i += 1
                text=""
                expected=[]
                continue

            el=re.split("\s+",line)
            if len(el)>1:
                expected.append((el[0],el[1] if el[1]!="O" else "OTHER"))
                text+=el[0]+" "

        save_results('outputs/testtagging.xlsx',all_results)
if __name__=='__main__':
    fileName="../corpus/samples/saieinput_sample.txt"
    sents_samples = open("../segtools/tools/hadith_corpus_pure_segmented.txt", "r", encoding="windows-1256").readlines()[
                 5000:6000]



    referenceTable={}
    unigramTagger=UnigramHMM(referenceTable)
    HmmModel=HMM(backoff=unigramTagger)
    trigHMM=TrigramHMM(backoff=HmmModel)

    #corpus=word_tag_from_files(position.replace("\\", "/") + "/../corpus/sources/emission",position)
    #trigHMM.train(corpus,test_size=0.2)

        # Test tagging sentences sample
    test_sentences_tag(trigHMM)

        # Test Tagging texts and outputing csv results
    #evaluation(trigHMM,sents_samples)

    
   












    
        
    
 