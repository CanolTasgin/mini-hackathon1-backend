import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import helper
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# to simplify the data access, we just use a .json for the template
FILE_PATH = "data/"
USER_DATA_PATH = FILE_PATH+"userdata.json"
SYMPTOM_DATA_PATH = FILE_PATH+"symptom.json"

try:
    user_email = os.getenv("SENDER_EMAIL")
except:
    print("""please define SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL and OPENAI_API_KEY in ENV VAR e.g
                please config your env:
                SENDER_EMAIL=humbertechsociety@gmail.com
                RECEIVER_EMAIL=humbertechsociety@gmail.com
                SENDER_PASSWORD=xxx
                OPENAI_API_KEY=xxx
            """ )

CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
  
@app.route("/data", methods=["GET"])
def get_data():
    with open(USER_DATA_PATH) as f:
        data = json.load(f)
    return jsonify(data)
  
@app.route("/add_data", methods=["POST"])
def add_data():
    symptom_name = request.json.get('symptom_name')
    print('symptom_name')
    print(symptom_name)
    symptom_data={}
    user_data={}
    with open(USER_DATA_PATH, "r") as f:
        print(user_email)
        user_data = json.load(f)
        if "symptom" not in user_data[user_email]:
            user_data[user_email]["symptom"] = {}
        print("user_data")
        print(user_data)
        with open(SYMPTOM_DATA_PATH, "r") as f:
            symptom_data = json.load(f)
            if symptom_name in symptom_data:
                current_time = datetime.now().strftime("%m/%d/%y %H:%M")
                if current_time not in user_data[user_email]["symptom"]:
                    user_data[user_email]["symptom"][current_time] = []
                # restructure
                new_symptom_data = {}
                new_symptom_data = symptom_data[symptom_name]
                new_symptom_data['name'] = symptom_name
                user_data[user_email]["symptom"][current_time].append(new_symptom_data)

                print('{} has been added'.format(symptom_name))
            else:
                return "no symptom info for {}".format(symptom_name)  

    with open(USER_DATA_PATH, "w") as f:
        json.dump(user_data, f)

    ### Comment this part if you dont want to setup the OPENAI and EMAIL
    alert_bool = helper.history_tracker(USER_DATA_PATH, user_email)
    if alert_bool:
        helper.send_email('Health Risk Alert!!')
    return "Done adding, {}!".format(symptom_name)
    ###


@app.route("/symptom", methods=["GET"])
def get_foods():
    with open(SYMPTOM_DATA_PATH) as f:
        foods = json.load(f)

    return jsonify(foods)

def init_userdata():
    # to skip the authentication, we just hardcode here for now
    user_data = ""

    with open(USER_DATA_PATH, "r") as f:
        user_data = json.load(f)
        # feel free to modify it
        if user_email not in user_data:
            user_data[user_email] = {
                    "id": 13,
                    "first_name": "Humber",
                    "last_name": "ABC",
                    "age": 27,
                    "height_cm": 170,
                    "weight_kg": 70
            }
        print(user_data)
    
    with open(USER_DATA_PATH, "w+") as f:
        json.dump(user_data, f)

if __name__ == "__main__":
    init_userdata()
    app.run(host='0.0.0.0', debug=True)

