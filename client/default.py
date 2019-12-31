from flask import Flask
from flask_restful import Api, Resource, reqparse, request
from flask import jsonify, make_response
import werkzeug
import simplejson as json
from flask_cors import CORS

import sys
import os
import inspect


currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir + "\\NLP\\model")

import models
from models import HMM
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

UPLOAD_FOLDER = './filesToTag'
parser = reqparse.RequestParser()
parser.add_argument(
    'file', type=werkzeug.datastructures.FileStorage, location='files')

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})


api = Api(app)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/hello', methods=['GET'])
def call():
    x = request.args.get('text')
    print(x)
    return "hello"


@app.route('/tag-text', methods=['POST'])
def tagText():
    try:

        content = request.get_json(force=True)
        # print(content)

        if (content["Function"] == "taggText"):

            tagged_words = HMM().tagText(content["Text"])
            response_body = {
                "Flag": "Sucess",
                "Result": json.dumps(tagged_words, encoding="windows-1256")
            }
            return make_response(jsonify(response_body), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({"Flag": "Fail",
                                      "Message": "An error has occured"+"\n \t"+str(e)
                                      }), 400)


@app.route('/tag-file', methods=['POST'])
def tagFile():	
    try:
        import random
        data = parser.parse_args()
        if (data['file'] == ""):
            
        	return {
        			'data':'',
        			'message':'No file found',
        			'status':'error'
        			}
        file = data['file']
        if (file):
        	filename = 'file'+str(random.randrange(1000))+'.txt'
        	file.save(UPLOAD_FOLDER+'/'+filename)
        	tagged_words=HMM().tagText(open(UPLOAD_FOLDER+'/'+filename,"r",encoding="utf8").read())
        	return {
        			'data':json.dumps(tagged_words, encoding="windows-1256"),
        			'message':'file uploaded',
        			'status':'success'
        			}
        return {
                  'data':'',
                  'message':'Something when wrong',
                  'status':'error'
                  }
    except Exception as e:
        print(e)
        return make_response(jsonify({"Flag": "Fail",
                                      "Message": "An error has occured"+"\n \t"+str(e)
                                      }), 400)

        

@app.route('/query-json', methods=['GET', 'POST'])
def add_message():
    content = request.get_json(force=True)
    print(content)
    if (content["Function"] == "taggText"):
        pass
    return 'ihab received the JSON '


# END'S of FAYÇAL suggestion

@app.route('/postjson', methods=['POST'])
def postJsonHandler():
    # we don't need to test bbut any way let's do it
    if request.is_json:
        # STORE THE RECEIVED JSON data in req
        req = request.get_json(force=True)
        # Here we pass req to HMM module
        # creating a dictionary to return it as a response to the client
        response_body = {
            "Message": "JSON received!",
            "Sender": req.get("name")
        }
        # CONVERT it to JSON and then we r returning json instead of Python dictionnary as well as we received JSON
        res = make_response(jsonify(response_body), 200)

        return res

    else:
        # in case of it's not a json data .. hedi dnia XD
        return make_response(jsonify({"Flag": "Fail", "Message": "Request body must be JSON"}), 400)


if __name__ == '_main_':
    while True:
        app.run(debug=True, port=5000)
