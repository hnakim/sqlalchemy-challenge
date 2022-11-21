import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#set up database
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#set up flask
app = Flask(__name__)

#flask routes
@app.route("/")
def home():
    """List all available api routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    ) 

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the last 12 months of prcp data."""
    # Create our session
    session = Session(engine)

    #precipitation query
    previous_year_date = dt.date(2017, 8 , 23) - dt.timedelta(days=365)
    previous_year_prcp = session.query(Measurement.date, Measurement.prcp)\
                                .filter(Measurement.date >=previous_year_date)\
                                .all()

    session.close()

    #create dictionary using date as key and prcp as value
    past_prcp = []
    for date, prcp in previous_year_prcp:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        past_prcp.append(prcp_dict)
   
    return jsonify(past_prcp)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    # Create our session
    session = Session(engine)

    #return a JSON list of stations from the dataset
    stations = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(stations))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations of the most-active station for the previous year."""
    # Create our session
    session = Session(engine)

    #query the dates and tobs from previous year
    previous_year_date = dt.date(2017, 8 , 23) - dt.timedelta(days=365)
    station_id = 'USC00519281'
    previous_year_temp = session.query(Measurement.tobs)\
                            .filter(Measurement.station == station_id)\
                            .filter(Measurement.date >= previous_year_date)\
                            .all()

    session.close()
    
    #return a JSON list of tobs for past year
    all_tobs = list(np.ravel(previous_year_temp))
    return jsonify(all_tobs)

# @app.route("/api/v1.0/<start>")
# def start():
#     # Create our session
#     session = Session(engine)
#     #query
#     start_date = 

#     session.close()
#     return 

# @app.route("/api/v1.0/<start>/<end>")
# def end():
#     # Create our session
#     session = Session(engine)
#     #query
#     session.close()
#     return 


if __name__ == "__main__":
    app.run(debug=True)
