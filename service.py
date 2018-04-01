from flask import Flask
from flask import request, redirect, url_for
import json
import base64
import os



app = Flask(__name__)
@app.route( "/", methods = ['POST'])
def poll():
    global user
    
    poll_id = base64.b64encode(os.urandom(32))

    user = request.form["user_id"]

    data = {
        "response_type": "in_channel",
        "attachments": [{
            "image_url": "http://www.europarl.europa.eu/downloadcentre/sites/europarl.europa.eu.downloadcentre/files/styles/epa_category_image/public/media/EP%20logo%20RGB_EN_0.png?itok=aOz0KQXC",
            "title": "New Document",
            "pretext": "Dear user, please note that there is a new survey you have to accept. Please accept the following document after reading it.",
            "text": "Please read the following anti-corruption document <http://www.example.com> and accept it by pressing the button below.",
            "actions": [{
                "name": "Yes, I have read it and accept it.",
                "integration": {
                    "url": "http://54.154.34.118:9000/vote",
                    "context": {
                        "action": "do_something_ephemeral"
                        }
                    }
            }],
            "fields": [{
                "title":"Description",
                "value":"With accepting the document you hereby confirm that you understand all rules.",
                "short":False
            }, {
                "title":"Please accept",
                "value":"Please click the button below. As soon as you accept your user_id will be submitted.",
                "short":True
            }],
        }]
    }

    response = app.response_class(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )

    return response

@app.route( "/vote", methods = ['POST'])
def vote():
    data = {
        "ephemeral_text": "You " + user + "updated the post!"
        }

    response = app.response_class(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )

    return response

@app.route("/update", methods = ['POST'])
def update():
    data = {
        "update": {
            "message": "Updated!"
            }
        }

    response = app.response_class(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )

    return response

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=9000, debug = True)
