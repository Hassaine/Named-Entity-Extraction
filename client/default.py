from flask import Flask
from flask_restful import Api,Resource,reqparse,request
from flask import jsonify, make_response


app = Flask(__name__)
api = Api(app)

@app.route('/query-example')
def query_example():
    return 'salut'
#This is the tag function suggested by FAYÇAL just to test nothing special
def tag(text):
    return text.replace("Some","Big")

@app.route('/tag-text', methods = ['GET'])
def tagText(text):
    try:
        content = request.get_json(force=True)
        if(content["Function"]=="taggText"):
            pass
    except:
        return make_response(jsonify({"Flag":"Fail","Message": "An error has occured"}), 400)    

@app.route('/query-json', methods=['GET', 'POST'])
def add_message():
    content = request.get_json(force=True)
    print (content)
    if(content["Function"]=="taggText"): 
        tagged=tag(content["Text"])
    return 'ihab received the JSON '+tagged
#END'S of FAYÇAL suggestion

@app.route('/postjson', methods = ['POST'])
def postJsonHandler():
    #we don't need to test bbut any way let's do it 
    if request.is_json:
        #STORE THE RECEIVED JSON data in req
        req = request.get_json(force=True)
        #Here we pass req to HMM module
        #creating a dictionary to return it as a response to the client
        response_body = {
            "Message": "JSON received!",
            "Sender": req.get("name")
        }
        #CONVERT it to JSON and then we r returning json instead of Python dictionnary as well as we received JSON
        res = make_response(jsonify(response_body), 200)

        return res

    else:
        #in case of it's not a json data .. hedi dnia XD
        return make_response(jsonify({"Flag":"Fail","Message": "Request body must be JSON"}), 400)


#LET'S THE HUNGER GAME BEGIIIIIIN'S
if __name__ == '_main_':
    app.run(debug=True,port=8000)