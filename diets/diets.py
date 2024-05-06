from flask import Flask, request, jsonify
from flask_restful import Api
import json
import pymongo
import sys

app = Flask(__name__)  # init Flask
api = Api(app)  # create API

# create DB
client = pymongo.MongoClient("mongodb://db-service:27017/")
db = client["myDB"]
# init collection diets in DB
diets_col = db["diets"]

if diets_col.find_one({"_id": 0}) is None:  # first time starting up this service as no document with _id ==0 exists
    # insert a document into the database to have one "_id" index that starts at 0 and a field named "cur_key"
    diets_col.insert_one({"_id": 0, "cur_key": 0})
    print("Inserted document containing cur_key with _id == 0 into the collection")
    sys.stdout.flush()

# support posting a new diet
def add_diet(diet_name, diet_cal, diet_sodium, diet_sugar):
    docID = {"_id": 0}
    cur_key = diets_col.find_one(docID)["cur_key"] + 1
    new_diet = {
    "name": diet_name,
    "cal": diet_cal,
    "sodium": diet_sodium,
    "sugar": diet_sugar,
    "ID": cur_key
    }
    diets_col.update_one(docID, {"$set": {"cur_key": cur_key}})
    diets_col.insert_one(new_diet)

# given a diet, this function returns it without it _id field
def remove_id(diet):
    updated_diet = {
        "name": diet.get("name"),
        "cal": diet.get("cal"),
        "sodium": diet.get("sodium"),
        "sugar": diet.get("sugar")
    }
    return updated_diet

# supports posting a new diet
@app.route('/diets', methods=['POST'])
def post_diet():
    data = request.get_json()
    diet_name = data["name"]
    diet = diets_col.find_one({"name": diet_name})
    # check if diet with this name already exists in collection
    if diet:
        return "Diet with name " + diet_name + " already exists", 422
    diet_cal, diet_sodium, diet_sugar = data["cal"], data["sodium"], data["sugar"]
    add_diet(diet_name, diet_cal, diet_sodium, diet_sugar)
    print("inserted diet with name " + diet_name + "successfully")
    sys.stdout.flush()
    return "Diet " + diet_name + " was created successfully", 201


# support retrieving all existing diets in json array format
@app.route('/diets', methods=['GET'])
def get_diets():
    diets = diets_col.find()
    # remove special first doc from output
    remove_doc = [item for item in diets if item["_id"] != 0]
    res = [remove_id(diet) for diet in remove_doc]
    # converts into json array
    print("Retrieving all diets:")
    print(json.dumps(res))
    sys.stdout.flush()
    return json.dumps(res), 200

# support retrieving a diet by name
@app.route('/diets/<string:diet_name>', methods=['GET'])
def get_diet(diet_name):
    diet = diets_col.find_one({"name": diet_name})
    if diet:
        modified = remove_id(diet)
        return json.dumps(modified), 200
    return "Diet " + diet_name + " not found", 404

if __name__ == '__main__':
    print("running diets.py")


