import nltk
from  indexes import *
from  stemer import *
from  tokenizer import *
from model.hmm import *

TOKENIZER=BasicTokenize()
STEMMER=BasicStemmer()
ARABIC_STOPWORDS_INDEX=ArabicStopWordsIndex(STEMMER)

STEMMER.setStopWordsIndex(ARABIC_STOPWORDS_INDEX)
tokens=TOKENIZER.tokenize("infile.txt")
print("Tokenization result : ",str(tokens))


print(HMM(STEMMER).constructTransitionMatrix(["NEtagSeq.txt"]))
#print(STEMMER.getStems(tokens))



