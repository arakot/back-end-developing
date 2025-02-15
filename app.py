from flask import Flask, jsonify, request # import the Flask class and other modules from the Flask package
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # create an instance of the Flask class

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # set the URI for the database  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # set the track modifications to false
app.config['JWT_SECRET_KEY'] = 'super-secret' # set the secret key for the JWT token

db=SQLAlchemy(app) # create an instance of the SQLAlchemy class
jwt = JWTManager(app) # create an instance of the JWTManager class

users = [
    {'id': 1, 'name': 'admin', "password": "password"},
    {'id': 2, 'name': 'Jane', "email": "Jane@gmail.com"}
] # list of users to be used in the application

class User(db.Model): # create a User class that inherits from db.Model
    id = db.Column(db.Integer, primary_key=True) # create a column for the id
    username = db.Column(db.String(50), unique=True, nullable=False) # create a column for the name
    password = db.Column(db.String(100), nullable=False) # create a column for the password
    name = db.Column(db.String(100), nullable=False) # create a column for the email

def to_dict(self): # create a method to convert the user object to a dictionary
    return {"id": self.id, "username": self.username, "password": self.password, "name": self.name} # return a dictionary with the user data

@app.route('/') # route() decorator to tell Flask what URL should trigger our function


def home(): 
    return "Hello, World!"

@app.route('/register', methods=['POST']) # route to register a new user
def register():
    data = request.get_json() # get the data sent with the POST request
    new_user = User(username=data['username'],password = data['password'], name = data['name']) # create a new user object
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201 # return a message and 201 status code which means the request was successful

@app.route('/login', methods=['POST']) # route to login a user
def login():
    data =request.get_json() # get the data sent with the POST request
    user = User.query.filter_by(username=data["username"], password=data["password"]).first() # search for the user by username and password 
  
    # username = data.get('name') # get the username from the data
    # password = data.get('password') # get the password from the data

    # user = next((user for user in users if user['name'] == username and user['password'] == password), None) # search for the user by username and password 
    if user: # if the user is found
        access_token = create_access_token(identity=user.username) # create an access token for the user
        return jsonify(access_token=access_token), 200 # return the access token and 200 status code which means the request was successful
    return jsonify({"message": "Invalid credentials"}), 401 # return a message and 401 status code which means the request was unauthorized
    

@app.route('/user', methods = ['POST']) # route to add a new user
def add_user(): # function to add a new user
    data = request.get_json() # get the data sent with the POST request
    new_user ={  # create a new user object
        'id': len(users)+1, # generate a new id for the new user
        'name': data['name'], # get the name of the new user from the request data
        'email': data['email'] # get the email of the new user from the request data    
            
    }
    users.append(new_user) # add the new user to the list of users
    return jsonify(new_user), 201 # 201 status code means that a new resource has been created
    

# @app.route('/user/<name>', methods = ['GET'])   # route to get a user by name
# def get_user(name):     # function to get a user by name
#     user = next((user for user in users if user['name'] == name), None)     # search for the user by 
#     if user:    # if the user is found
#         return jsonify(user), 200    # return the user and 200 status code  which means the request was successful
#     return  jsonify({"message": "User not found"}), 404     # return a message and 404 status code which means the resource was not found   

@app.route('/users', methods=['GET']) # route to get all users
@jwt_required() # require a JWT token to access this route
def get_users(): # function to get all users
    users=User.query.all() # get all the users from the database
    users_list = [{"id": user.id, "username": user.username, "name": user.name} for user in users]
    return jsonify(users_list), 200 # return the users and 200 status code which means the request was successful

@app.route('/user/<int:id>', methods=['DELETE']) # route to delete a user by id
@jwt_required() # require a JWT token to access this route
def delete_user(id): # function to delete a user
    user= User.query.get(id) # get the user by id
    # user = next((user for user in users if user['id'] == id), None) # search for the user by id
    if user: # if the user is found
       db.session.delete(user) # delete the user from the database
       db.session.commit()
       # users.remove(user) # remove the user from the list of users
       return jsonify({"message": "User deleted"}), 200 # return a message and 200 status code which means the request was successful
    return jsonify({"message": "User not found"}), 404 # return a message and 404 status code which means the resource was not found


@app.route('/user/<int:id>', methods=['PUT']) # route to update a user
@jwt_required() # require a JWT token to access this route
def update_user(id): # function to update a user
    data = request.get_json() # get the data sent with the PUT request
    user=User.query.get(id)
    # user = next((user for user in users if user['id'] == id), None) # search for the user by id 
    if user: # if the user is found
        user.name = data.get("name", user.name)
        user.username = data.get("username", user.username)
        db.session.commit()
        
        # user['name'] = data['name'] # update the user's name
        # user['email'] = data['email'] # update the user's email
        return jsonify({"message": "User updated successfully", "name": user.name, "username": user.username}), 200  # return success with user data
    return jsonify({"message": "User not found"}), 404
        
if __name__=="__main__":    # If the script is executed directly, the code block will be executed.
    app.run(debug=True) # run the application on the local development server
