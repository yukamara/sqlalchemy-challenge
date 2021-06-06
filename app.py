
#################################################
# Import dependencies
#################################################
import pandas as pd
import datetime as dt
import numpy as np

#################################################
# Python SQL toolkit and Object Relational Mapper
#################################################
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes"""
    return (
        f"Welcome to my SQLAlchemy Challenge homepage, availble routes are:<br>"
        f"/api/v1.0/precipitation <br>"
        f"/api/v1.0/stations <br>"
        f"/api/v1.0/tobs <br>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )    

##################################################
# Jsonifying Precipitation Query Results
##################################################

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all Measurements and close session
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Create a dictionary from the row data and append to a list of precipitation
    precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation) 

###################################################
#Jsonifying Station Query Results
###################################################

@app.route('/api/v1.0/stations')
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all Stations and close session
    results = session.query(Station.id, Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()
    session.close()

    stations = []
    for id, station, name, latitude,longitude,elevation in results:
        station_dict = {}
        station_dict["id"] = station
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        stations.append(station_dict)

    return jsonify(stations)

###################################################
#Jsonifying Temperature Observation Query Results
###################################################

@app.route('/api/v1.0/tobs')
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all temperature data in the last year and close session
    date_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    result = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= date_year_ago).all()
    session.close()

    tempall = []
    for date, tobs in result:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temp"] = tobs
        tempall.append(tobs_dict)

    return jsonify(tempall)

###################################################
#Jsonifying Min, Max & Avg Temp: Start Only
###################################################

@app.route('/api/v1.0/<start>')
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for the min, max, & avg on or after start
    min_max_avg = session.query(func.min(Measurement.tobs),\
              func.max(Measurement.tobs),\
              func.avg(Measurement.tobs))\
              .filter(Measurement.date >= start).all()
    session.close()

    starttemps = []
    for min,avg,max in min_max_avg:
        temps_dict = {}
        temps_dict["min"] = min
        temps_dict["average"] = avg
        temps_dict["max"] = max
        starttemps.append(temps_dict)

    return jsonify(starttemps)


###################################################
#Jsonifying Min, Max & Avg Temp: btw Start & end
###################################################
@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start,end):

    session = Session(engine)


    # Query for the min, max, & avg for start and end dates
    min_max_avg = session.query(func.min(Measurement.tobs),\
              func.max(Measurement.tobs),\
              func.avg(Measurement.tobs))\
              .filter(Measurement.date >= start)\
              .filter(Measurement.date <= end).all()
    session.close()


    startendtemps = []
    for min,avg,max in min_max_avg:
        temp_dict = {}
        temp_dict["Min"] = min
        temp_dict["Average"] = avg
        temp_dict["Max"] = max
        startendtemps.append(temp_dict)

    return jsonify(startendtemps)


if __name__ =="__main__":
    app.run(debug=True)