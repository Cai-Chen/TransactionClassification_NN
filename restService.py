from flask import Flask, jsonify, abort, make_response, request
import tensorflow as tf
import classify

app = Flask(__name__)

@app.route('/')
def index():
    return "Classify the transaction according to description!"

@app.route('/title/<string:title>', methods=['GET'])
def get_task(title):
    category = classify.main(title)
    return jsonify({'category' : category}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
