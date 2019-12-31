
import os
import glob
import inspect
import re
import sys
import ast
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
sys.path.append(parentdir+"\\NLP\\model")
sys.path.append(parentdir+"\\NLP\\corpus")
sys.path.append(parentdir+"\\NLP\\segtools")








try:
     rawiINDC = open('./rawiINDC.txt','r',encoding="windows-1256").read().split()
     directoryListOfFile={}
     os.chdir(currentdir.replace("\\", "/") + "/../NLP/corpus/sources/emission/hadith")
     textfiles = [os.path.abspath(el) for el in list(glob.glob("*.txt"))]
     for file in textfiles:
        corpus = open(file,'r',encoding="windows-1256")
        objectBookSummery = { "rowat":{}}
        bookTitleFound=False
        bookTitle=""
        for line in corpus:       
            line=line[:-1].split()
            if(len(line)>1 and line[1]=='Book' and not bookTitleFound):
		 		
                while(line[1]=='Book'):               
                    bookTitle +=line[0]+" "
                    line = corpus.readline().split()               
            objectBookSummery["bookTitle"]=bookTitle   
            bookTitleFound=True
		 		
            if(len(line)>1 and line[1]=="O"):
                if(line[0] in rawiINDC):
		 			
                    line = corpus.readline().split() 
                    if(len(line) > 1 and line[1]=="PERSON"):
                        person=[]
		 				
                        while(len(line) > 1 and line[1]=='PERSON'):
		 				
		 					
                            person.append(line[0])
                            line = corpus.readline().split() 
                        if(objectBookSummery["rowat"].get(str(person),None) is None):    
                            objectBookSummery["rowat"][str(person)]=1
                        else:
                            objectBookSummery["rowat"][str(person)] += 1
		 					
		 				
        roawtNames=[ast.literal_eval(rawi) for rawi  in objectBookSummery['rowat']]
        rowatFreq=list(objectBookSummery['rowat'].values())   
        objectBookSummery['rowatNames']=roawtNames
        objectBookSummery['rowatFreq']=rowatFreq
        del objectBookSummery['rowat']
        directoryListOfFile.append(objectBookSummery)
        
     os.chdir(currentdir)
except FileNotFoundError as notFE:
     print("file does not exist !.")
     print(notFE.strerror())
  


#roawtNames=[ast.literal_eval(rawi) for rawi  in objectBookSummery['rowat']]
#
#rowatFreq=list(objectBookSummery['rowat'].values())


#for rawi in objectBookSummery['rowat'].keys():
#    print(ast.literal_eval(rawi))
#    print(objectBookSummery['rowat'][rawi])
#    break
#for rawi in objectBookSummery['rowat'].values():
#    print(rawi)
#    break


















# import tokenizer
# import models
# contexts = ['hadith']
# for context in contexts:
#     results = {}
#     sentsCpt = wordsCpt = 0
#     contextStats = {}
#     for context in contexts:
#         contextStats[context] = {}
#         try:
#             os.chdir(currentdir.replace("\\", "/") +
#                      "/../NLP/corpus/contexts/" + context)
#         except FileNotFoundError as notFE:
#             print("context does not exist !.")

#             continue

#         textfiles = [os.path.abspath(el) for el in list(glob.glob("*.txt"))]

#         for file in textfiles:
#             with open(file, "r", encoding="windows-1256") as f:

#                 sentences = re.findall("<S>.*?<E>", f.read())
#                 for sentence in sentences:
#                     sentsCpt += 1
#                     sentence = re.sub("<S>|<E>", "", sentence)
#                     words = tokenizer.BasicTokenize().tokenize(sentence)
#                     wordsCpt += len(words)

#         contextStats[context]["AVGWordsPersSents"] = wordsCpt / sentsCpt
#         contextStats[context]["AVGSentsPerContext"] = sentsCpt / len(textfiles)

#         os.chdir(currentdir)
# print(contextStats)
