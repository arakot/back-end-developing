from flask import Flask

app = Flask(__name__) # create an instance of the Flask class
@app.route('/') # route() decorator to tell Flask what URL should trigger our function

def home(): 
    return "Hello, World!"

if __name__=="__main__":    # If the script is executed directly, the code block will be executed.
    app.run(debug=True) # run the application on the local development server