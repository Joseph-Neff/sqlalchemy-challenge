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
    session = Session(engine)

    """Return a list of all Precipitation Data"""
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-24").\
        all()
    
    all_prcp = []
    for date,prcp  in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station).\
                 order_by(Station.station).all()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year).\
        order_by(Measurement.date).all()

    list_tobs_data = list(tobs_data)

    return jsonify(list_tobs_data)

@app.route("/api/v1.0/<start>")
def start_date(start):

    start_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()

    list_start_date = list(start_date)

    return jsonify(list_start_date)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):

    start_end_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        group_by(Measurement.date).all()
    
    list_start_end_date = list(start_end_date)

    return jsonify(list_start_end_date)

if __name__ == '__main__':
    app.run(debug=True)