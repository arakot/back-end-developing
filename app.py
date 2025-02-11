from flask import Flask, jsonify, request

app = Flask(__name__) # create an instance of the Flask class


users = [
    {'id': 1, 'name': 'John'},
    {'id': 2, 'name': 'Jane'}
]

@app.route('/') # route() decorator to tell Flask what URL should trigger our function


def home(): 
    return "Hello, World!"


@app.route('/user', methods = ['POST'])
def add_user():
    data = request.get_json()
    new_user ={
        'id': len(users)+1,
        'name': data['name']
    }
    users.append(new_user)
    return jsonify(new_user), 201
    

@app.route('/user/<name>', methods = ['GET'])
def get_user(name):
    user = next((user for user in users if user['name'] == name), None)
    if user:
        return jsonify(user), 200
    return  jsonify({"message": "User not found"}), 404
    
if __name__=="__main__":    # If the script is executed directly, the code block will be executed.
    app.run(debug=True) # run the application on the local development server
