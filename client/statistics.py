# -*- coding: utf-8 -*-
"""
Created on Wed Dec  14 23:41:18 2019

@author: Selmane
"""
import sqlalchemy.sql.functions
from flask import Flask
from flask_restful import Api, Resource, reqparse, request
from flask_cors import CORS
from flask import jsonify, make_response
import os, sys, inspect,glob,re
import simplejson as json
import nltk
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
sys.path.append(parentdir+"\\NLP\\model")
sys.path.append(parentdir+"\\NLP\\corpus")
sys.path.append(parentdir+"\\NLP\\segtools")


import models
import tokenizer

'''app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
api = Api(app)'''


#@app.route('/words-sents')
def words_sents_stats():
    return "Hello World!"


#@app.route('/words-sents')
def words_sents_stats(contexts=["hadith"]):
    for context in contexts:
        results = {}
        sentsCpt = wordsCpt = 0
        contextStats = {}
        for context in contexts:
            contextStats[context] = {}
            try:
                os.chdir(currentdir.replace("\\", "/") + "/../NLP/corpus/contexts/" + context)
            except FileNotFoundError as notFE:
                print("context does not exist !.")

                continue

            textfiles = [os.path.abspath(el) for el in list(glob.glob("*.txt"))]

            for file in textfiles:
                with open(file, "r", encoding="windows-1256") as f:

                    sentences = re.findall("<S>.*?<E>", f.read())
                    for sentence in sentences:
                        sentsCpt += 1
                        sentence = re.sub("<S>|<E>", "", sentence)
                        words = tokenizer.BasicTokenize().tokenize(sentence)
                        wordsCpt += len(words)

            contextStats[context]["AVGWordsPersSents"] = wordsCpt / sentsCpt
            contextStats[context]["AVGSentsPerContext"] = sentsCpt / len(textfiles)


            os.chdir(currentdir)


    response_body = {
        "Flag": "Sucess",
        "Result": json.dumps(contextStats)
    }
    return make_response(jsonify(response_body), 200)



#@app.route('/ne-tagged-stats')
def tagged_ne_stats():
    root,dirs,fileNames=list(os.walk(currentdir.replace("\\", "/") + "/../NLP/corpus/taggedTexts/contexts"))[0]
    contextStats={}
    for dir in dirs:
        contextStats[dir] = {}
        try:
            os.chdir(os.path.abspath(dir))

        except FileNotFoundError as notFE:
            print("NeTaggedStats : \t context '",dir.upper(), "'  does not exist !.")

            continue

        textfiles = [os.path.abspath(el) for el in list(glob.glob("*.txt"))]

        for file in textfiles:
            with open(file, "r", encoding="windows-1256") as f:

                sentences = re.findall(".", f.read())
                for sentence in sentences:
                    sentsCpt += 1
                    sentence = re.sub("<S>|<E>", "", sentence)
                    words = tokenizer.BasicTokenize().tokenize(sentence)
                    wordsCpt += len(words)

        contextStats[dir]["AVGWordsPersSents"] = wordsCpt / sentsCpt
        contextStats[dir]["AVGSentsPerContext"] = sentsCpt / len(textfiles)

        os.chdir(currentdir)










ne_stats()
#words_sents_stats(["hadith"])