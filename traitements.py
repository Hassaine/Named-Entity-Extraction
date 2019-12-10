import nltk
from  indexes import *
from  stemer import *
from  tokenizer import *

TOKENIZER=BasicTokenize()
STEMMER=BasicStemmer()
ARABIC_STOPWORDS_INDEX=ArabicStopWordsIndex(STEMMER)

tokens=TOKENIZER.tokenize("infile.txt")
print("Tokenization result : ",str(tokens))

#print(STEMMER.getStems(tokens))



