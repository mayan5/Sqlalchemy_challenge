# 1. import Flask
import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify 
from sqlalchemy import desc



Base = automap_base()
engine = create_engine("sqlite:///C:/Users/Marisabel Matta/Desktop/hawaii.sqlite",echo= False)
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station
session = Session(engine)


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- List of prior year rain totals from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of Station numbers and names<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- List of prior year temperatures from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"- When given the start date (YYYY-MM-DD), calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"- When given the start and the end date (YYYY-MM-DD), calculate the MIN/AVG/MAX temperature for dates between the start and end date inclusive<br/>"
    )

    



# 4. Define what to do when a user hits the /about route
@app.route("//api/v1.0/precipitation")
def precipitation():
    precep_scores = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date > '2016-08-22').\
    order_by(measurement.date).all()
    rain_totals = []
    for result in precep_scores:
        row = {}
        row["date"] = precep_scores[0]
        row["prcp"] = precep_scores[1]
        rain_totals.append(row)

    return jsonify(rain_totals)


@app.route("//api/v1.0/stations")
def stations():
    results = session.query(measurement.station).group_by(measurement.station).all()
    all_sessions = list(np.ravel(results))
    return jsonify(all_sessions)


@app.route("//api/v1.0/tobs")
def tobs():
    active_station_scores = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date > '2016-08-24').all()
    tobs_list = []
    for score in active_station_scores:
        row = {}
        row["date"] = score[0]
        row["tobs"] = score[1]
        tobs_list.append(row)
    return jsonify(tobs_list)

@app.route("//api/v1.0/<start>")
def trip1(start):

 # go back one year from start date and go to end of data for Min/Avg/Max temp   
    start_date= dt.datetime.strptime(start,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    trip_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)



@app.route("//api/v1.0/<start>/<end>")
def trip2(start,end):

 # go back one year from start date and go to end of data for Min/Avg/Max temp   
    start_date1= dt.datetime.strptime(start,'%Y-%m-%d')
    last_year1 = dt.timedelta(days=365)
    end_date1= dt.datetime.strptime(end,'%Y-%m-%d')
    start1 = start_date1-last_year1
    end1 = end_date1-last_year1
    trip_data2 = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start1).filter(measurement.date <= end1).all()
    trip2 = list(np.ravel(trip_data2))
    return jsonify(trip2)






if __name__ == "__main__":
    app.run(debug=True)
