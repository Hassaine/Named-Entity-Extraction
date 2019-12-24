import nltk



class ArabicStopWordsIndex:
    def __init__(self,stemmer):
        self.stemmer=stemmer
        self.index=None


    def buildIndex(self):
        arabic_stopwords = set(nltk.corpus.stopwords.words("arabic"))
        self.index=nltk.defaultdict(list)
        for word in arabic_stopwords:
            self.index[word[0]].append(word)


        return self.index


    def access(self,word):
        if self.index is None or  not bool(self.index):
            self.index=self.buildIndex()

        try:
            word=word.encode("utf-8").decode("windows-1256")
        except UnicodeEncodeError as encodeErr:

            print("Encoding/Decoding Error : on Access() method.")
            print("\t",encodeErr)
            return

        word=self.stemmer.norm(word)
        if word[0] not in self.index:
            return False

        return word in self.index[word[0]]
