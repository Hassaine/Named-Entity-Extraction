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

BASE_CONTEXT_DIRECTORY =parentdir+"\\NLP\\corpus\\contexts"
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
api = Api(app)





@app.route('/words-sents')
def words_sents_stats():
    contexts = request.args.get("hadith")
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



@app.route('/ne-tagged-stats')
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

@app.route('/corpus-texts-content',methods=['GET','POST'])
def get_corpus_text():
    try:
        narator=None
        context=request.args.get('context')
        if "narator" in request.args:
            narator=request.args.get("narator")

        print(list(os.walk(BASE_CONTEXT_DIRECTORY))[0])
        dirs=list(os.walk(BASE_CONTEXT_DIRECTORY))[0][1]

        if context not in dirs:
            return make_response(jsonify({"Flag": "Fail",
                                          "Message": "No corpus found for the specific context"
                                          }), 400)
        textFiles = [os.path.abspath(el) for el in list(glob.glob(BASE_CONTEXT_DIRECTORY+"\\"+context+"\\*.txt"))]
        if narator is None: narator=""
        listTexts=[]
        for file in textFiles:
            with open(file,"r",encoding="windows-1256") as f:
                texts=f.read().split("<H>")
                for text in texts:
                    if narator in text:
                        listTexts.append(text)

                f.close()

        return make_response(jsonify({"Flag": "Success",
                                      "result": listTexts
                                      }), 200)
    except Exception as e:

        return make_response(jsonify({"Flag": "Fail",
                                      "Message": "An error has occured" + "\n \t" + str(e)
                                      }), 400)










#ne_stats()
#words_sents_stats(["hadith"])