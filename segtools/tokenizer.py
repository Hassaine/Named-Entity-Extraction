import nltk
from nltk.corpus import words
from nltk import WordPunctTokenizer
from nltk.tokenize import RegexpTokenizer
import re


class BasicTokenize:

    def __init__(self):
        pass


    def tokenizeFrom(self, fileInput, encoding="windows-1256"):
        text = open(fileInput, "r", encoding=encoding).read()

        # tokens=WordPunctTokenizer().tokenize(text)
        # tokens=nltk.tokenize.regexp_tokenize(text,r"[^\s,;\.،…:\(\)\[\]!\?؟’\n\"'\+\*\\/%=<>«»]+")
        tokens = nltk.tokenize.regexp_tokenize(text, r"[^\s,;،…:\(\)\[\]!\?؟’\n\"'\+\*\\/%=<>«»]+")
        tokens = [re.sub(r"\s+|\.+$", "", el) for el in tokens]
        tokens = [el for el in tokens if el != ""]

        tt = u"\x0033 \x8D \x8E \x90 \xC1- \xD6 \xD8- \xDF \xE1 \xE3- \xE6 \xEC- \xED \xF0- \xF3 \xF5 \xF6 \xF8 \xFA".split()
        stt = u"\xD8"
        # stt=stt.encode("windows-1256").decode("utf-8")
        return tokens

    def tokenize(self, text):
        # tokens=WordPunctTokenizer().tokenize(text)
        # tokens=nltk.tokenize.regexp_tokenize(text,r"[^\s,;\.،…:\(\)\[\]!\?؟’\n\"'\+\*\\/%=<>«»]+")
        tokens = nltk.tokenize.regexp_tokenize(text, r"[^\s,;،…:\(\)\[\]!\?؟’\n\"'\+\*\\/%=<>«»]+")
        tokens = [re.sub(r"\s+|\.+$", "", el) for el in tokens]
        tokens = [el for el in tokens if el != ""]

        return tokens
