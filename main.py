from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize Flask app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100), unique=True)

    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'contact')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Add New User
@app.route('/user', methods=['POST'])
def add_user():
    name = request.json['name']
    contact = request.json['contact']

    new_user = User(name, contact)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201  # HTTP 201 Created

# Show All Users
@app.route('/user', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result), 200  # HTTP 200 OK

# Show User by ID
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404  # HTTP 404 Not Found
    return user_schema.jsonify(user), 200  # HTTP 200 OK
 #Update User
 
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    user.name = request.json['name']
    user.contact= request.json['contact']
    db.session.commit()
    return user_schema.jsonify(user)

# Delete User

@app.route('/user/<id>', methods=["DELETE"])
def delete_user(id):
    user=User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

# Run the application

if __name__ == '__main__':
    # Set debug mode and specify a custom port
    app.run(debug=True, port=5001)
