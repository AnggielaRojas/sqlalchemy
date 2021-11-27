
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from sqlalchemy.sql.expression import all_

engine = create_engine("sqlite:///hawaii.sqlite")


Base = automap_base()

Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station



app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(measurements.date).order_by(measurements.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp = session.query(measurements.date, measurements.prcp).filter(measurements.date > last_year).\
        order_by(measurements.date).all()

   prcp_total = []
    for result in prcp:
        row = {}
        row["date"] = prcp[0]
        row["prcp"] = prcp[1]
        prcp_total.append(row)

    return jsonify(prcp_total)

@app.route("/api/v1.0/stations")
def stations():
    stations_query = session.query(station.name, station.station)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
    return jsonify(stations.to_dict())

@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(measurements.date).order_by(measurements.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperature = session.query(measurements.date, measurements.tobs).filter(measurements.date > last_year).\
        order_by(measurements.date).all()

    temperature_totals = []
    for result in temperature:
        row = {}
        row["date"] = temperature[0]
        row["tobs"] = temperature[1]
        temperature_totals.append(row)

    return jsonify(temperature_totals)

    @app.route("/api/v1.0/<start>")
def start_(start):
 
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    start_data = session.query(func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)).filter(measurements.date >= start).filter(measurements.date <= end).all()
    results = list(np.ravel(start_data))
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def starts_end(start,end):
 
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    end_data = session.query(func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)).filter(measurements.date >= start).filter(measurements.date <= end).all()
    results = list(np.ravel(end_data))
    return jsonify(results)


    calc = []
    for min, avg, max in results:
        end_dict = {}
        end_dict["min :"] = min
        end_dict["average :"] = avg
        end_dict["max :"] = max

    calc.append(end_dict)

    return jsonify(calc)

if __name__ == "__main__":
    app.run(debug=True)