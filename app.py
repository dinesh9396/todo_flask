from flask import Flask, request, jsonify
from flask_pymongo import PyMongo   
from flask_cors import CORS
# import os
from bson.objectid import ObjectId
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://mldinesh0:DPGq3M5xFkYGKfD6@cluster0.mnugi39.mongodb.net/mydatabase?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"

mongo = PyMongo(app)
CORS(app)

@app.route('/todos', methods=['GET'])
def get_all_todos():
    todos = mongo.db.todos
    result = []
    for field in todos.find():
        result.append({'_id': str(field['_id']), 'todo': field['todo']})
    return jsonify(result)


@app.route('/todo', methods=['POST'])
def add_todo():
    todos = mongo.db.todos
    todo = request.json['todo']
    # result = todos.insert_one({'todo': todo}) 
    result = todos.insert_one({'todo': todo, 'completed': False}) 
    todo_id = result.inserted_id  
    new_todo = todos.find_one({'_id': todo_id })
    return jsonify({'_id': str(new_todo['_id']), 'todo': new_todo['todo']})


@app.route('/todo/<id>', methods=['PUT'])
def update_todo(id):
    print("Updating todo with id: ", id)
    todos = mongo.db.todos
    todo = request.json['todo']
    # todos.update_one({'_id': ObjectId(id)}, {"$set": {'todo': todo}}, upsert=False)
    todos.update_one({'_id': ObjectId(id)}, {"$set": {'todo': todo, 'completed': False}}, upsert=False)
    updated_todo = todos.find_one({'_id': ObjectId(id)})
    return jsonify({'_id': str(updated_todo['_id']), 'todo': updated_todo['todo']})

@app.route('/todo/<id>/complete', methods=['PUT'])
def complete_todo(id):
    todos = mongo.db.todos
    completed = request.json['completed']
    todos.update_one({'_id': ObjectId(id)}, {"$set": {'completed': completed}}, upsert=False)
    completed_todo = todos.find_one({'_id': ObjectId(id)})

    # Add check for None
    if completed_todo is None:
        return jsonify({"error": "No todo found with the given id"}), 404

    return jsonify({'_id': str(completed_todo['_id']), 'todo': completed_todo['todo'], 'completed': completed_todo['completed']})


@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    print("Deleting todo with id: ", id)
    todos = mongo.db.todos
    result = todos.delete_one({'_id': ObjectId(id)})
    
    if result.deleted_count == 1:
        response = {'status': 'success'}
    else:
        response = {'status': 'error'}
    return jsonify(response)

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
    app.run(debug=True)
