
"""


@author: hassaine
"""
import os, sys, inspect,glob,re
from flask import Flask
from flask_restful import Api, Resource, reqparse, request
from flask_cors import CORS
from flask import jsonify, make_response
import simplejson as json

currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
sys.path.append(parentdir+"\\NLP\\corpusManager")


from corpusManager import corpusManager


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:*"}})
api = Api(app)

@app.route('/corpus', methods=['GET'])

def getcorpus():
    try:
        corpusName=request.args.get('corpusName')
        myCorpusManager = corpusManager()
        corpus = myCorpusManager.getCorpusJSON(corpusName)

        response_body = {
                    "Flag": "Sucess",
                    "Result": json.dumps(corpus, encoding="windows-1256")
                }
        return make_response(jsonify(response_body), 200) 


    except Exception as e:
        print("file does not exist !.")
        return make_response(jsonify({"Flag": "Fail",
                                      "Message": "An error has occured"+"\n \t"+str(e)
                                      }), 400)
        print(e.strerror)




@app.route('/addword', methods=['POST'])
def addWord():
    try:
        corpusName=request.args.get('corpusName')
        word= request.get_json(force=True)
        myCorpusManager = corpusManager()
        myCorpusManager.insert(corpusName=corpusName,wordObject=word)
        response_body = {
                    "Flag": "Sucess",
                    "Result": "inserted in the corpus "+corpusName
                }
        return make_response(jsonify(response_body), 200) 


    except Exception as e:
        print("file does not exist !.")
        return make_response(jsonify({"Flag": "Fail",
                                      "Message": "An error has occured"+"\n \t"+str(e)
                                      }), 400)
        print(e.strerror)
  




@app.route('/updateword', methods=['POST'])
def updateWord():
    try:
        corpusName=request.args.get('corpusName')
        word= request.get_json(force=True)
        myCorpusManager = corpusManager()
        myCorpusManager.update(corpusName=corpusName,wordObject=word)
        response_body = {
                    "Flag": "Sucess",
                    "Result": "the corpus "+corpusName+" has been updated"
                }
        return make_response(jsonify(response_body), 200) 


    except Exception as e:
        print("file does not exist !.")
        return make_response(jsonify({"Flag": "Fail",
                                      "Message": "An error has occured"+"\n \t"+str(e)
                                      }), 400)
        print(e.strerror)



@app.route('/words', methods=['DELETE'])
def deleteWord():

    try:
        word=request.args.get('word')
        corpusName=request.args.get('corpusName')

        myCorpusManager = corpusManager()
        myCorpusManager.delete(corpusName=corpusName,word=word)
        response_body = {
                    "Flag": "Sucess",
                    "Result": "the word "+word+" has been deleted from "+corpusName
                }
        return make_response(jsonify(response_body), 200) 


    except Exception as e:
        print("file does not exist !.")
        return make_response(jsonify({"Flag": "Fail",
                                      "Message": "An error has occured"+"\n \t"+str(e)
                                      }), 400)
        print(e.strerror)
    
    


if __name__ == '_main_':
    while True:
        app.run(debug=True, port=4200)