from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['smart_fridge']
collection = db['items']

@app.route('/items', methods=['GET'])
def get_items():
    items = list(collection.find({}, {'_id': 0}))
    return jsonify(items)

@app.route('/items', methods=['POST'])
def add_item():
    item = request.json
    item['expiration_date'] = datetime.strptime(item['expiration_date'], '%Y-%m-%d')
    collection.insert_one(item)
    return jsonify({'msg': 'Item added'}), 201

@app.route('/items/<name>', methods=['DELETE'])
def delete_item(name):
    collection.delete_one({'name': name})
    return jsonify({'msg': 'Item deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
