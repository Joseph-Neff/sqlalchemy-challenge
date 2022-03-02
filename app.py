import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Station= Base.classes.station
Measurement = Base.classes.measurement

app = Flask(__name__)

@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"Precipitaion: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"dates and temperature observations of the most active station for the last year of data: /api/v1.0/tobs<br/>"
        f"Temperature from start date(format:yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature from start to end date(format:yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session
    session = Session(engine)

    """Return a list of all Precipitation Data"""
    # Query all Precipitation
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-24").\
        all()

    session.close()
    
    # Convert list to Dictionary
    all_prcp = []
    for date,prcp  in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)