from flask import Flask, jsonify, abort, make_response, request
import tensorflow as tf
import classify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return "Classify the transaction according to description!"

@app.route('/getCategory', methods=['POST'])
def get_category():
    if not request.json or not 'title' in request.json:
        abort(400)
    category = classify.main(request.json['title'])
    return jsonify({'category' : category}), 201

@app.route('/inputCategory', methods=['POST'])
def input_category():
    if not request.json or not 'title' in request.json or not 'category' in request.json:
        abort(400)
    # Add new data to training set
    with open('./txn-data_modified.json', 'r', encoding='utf-8') as load_f:
        load_json = json.load(load_f)
        load_json.append({"title" : request.json['title'], "category" : request.json['category']})
    with open('./txn-data_modified.json', 'w', encoding='utf-8') as dump_f:
        json.dump(load_json, dump_f)
    return jsonify({'response' : 'updated'}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
