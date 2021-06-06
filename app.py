# Import Flask
from flask import Flask, jsonify

#Create an app
app = Flask(__name__)

# Define what to do when a user hits the home page route
@app.route("/")
def home():
    return (
        f"Welcome to my SQLAlchemy Challenge homepage, availble routes are:<br>"
        f"/api/v1.0/precipitation <br>"
        f"/api/v1.0/stations <br>"
        f"/api/v1.0/tobs <br>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>"
    )    

if __name__ =="__main__":
    app.run(debug=True)