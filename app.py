# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()


# reflect an existing database into a new model
Base.prepare(autoload_with=engine)
# reflect the tables

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        )

@app.route("/api/v.1.0/precipitation")
def precip():
    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    most_recent = "2017-08-23"
    analysis_query = session.query(Measurement.date, Measurement.prcp).\
     filter(Measurement.date <= most_recent).\
     filter(Measurement.date >= query_date).all()
    
    session.close()
    dict1 = {}
    precipitation_data = {date: prcp for date, prcp in analysis_query}

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Measurement.station.distinct()).all()
    session.close()
    list_stations = [res[0] for res in results]

    return jsonify(list_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_active_station = session.query(Measurement.station,func.count(Measurement.station)).\
    order_by(func.count(Measurement.station).desc()).\
    group_by(Measurement.station).first()

   
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    most_recent = "2017-08-23"

    
    results = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.station == most_active_station[0],
        Measurement.date >= query_date
    ).all()
    temperature_data = [{"date": date, "temperature": tobs} for date, tobs in results]

    return jsonify(temperature_data)
# @app.route("/api/v1.0/<start>")
# def xfunc():
#     return""

if __name__ == "__main__":
    app.run(debug=True)