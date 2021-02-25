from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt
import numpy as np

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
# @TODO: Initialize your Flask app here
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Home page
@app.route('/')
def home_page():
    return(
        f'Welcome to the weather app!<br/>'
        f'---------------------------<br/>'
        f'Available api routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/temp/start_date<br/>'
        f'/api/v1.0/temp/start_date/end_date<br/>'
    )



@app.route('/api/v1.0/precipitation')
def precipitation(): 

    session = Session(engine)
    # Query 12 months of data
    year_ago=dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    session.close()


    # Convert the query results to a dictionary using date as the key and prcp as the value.
    prcp_dict = {}
    for date, prcp in results:     
        prcp_dict[date] = prcp

    # Return the JSON representation of your dictionary.
    return jsonify(prcp_dict)


@app.route('/api/v1.0/stations')
def stations():
# Return a JSON list of stations from the dataset.
    session = Session(engine)

    results=session.query(Station.id, Station.station).all()

    session.close()

    station_dict = {}
    for station_id, station_name in results:     
        station_dict[station_id] = station_name

    return jsonify(stations=station_dict)


@app.route('/api/v1.0/tobs')
def tobs():
# # # Query the dates and temperature observations 
    session = Session(engine)

    year_ago=dt.date(2017, 8, 23) - dt.timedelta(days=365)

    station_results=session.query(Measurement.date, Measurement.tobs)\
                    .filter(Measurement.station=='USC00519281')\
                    .filter(Measurement.date >= year_ago).all()

    session.close()
# # # Return a JSON list of temperature observations (TOBS) 
# # for the previous year.
    active_dict = {}
    for date, tobs in station_results:     
        active_dict[date] = tobs

# Return the JSON representation of your dictionary.
    return jsonify(USC00519281=active_dict)



# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""
    session = Session(engine)
    # Select statement to simplify query:
    # calculate TMIN, TAVG, TMAX for dates to filter by later
    sel = [func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)]

    # if no end date is provided, only filter by start date
    if not end:
        
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()

    # if end and start date provided, filter by both
    else:
        results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()


    temp_dict={}
    for min, avg, max in results:
        temp_dict['min']=min
        temp_dict['avg']=avg
        temp_dict['max']=max

    return jsonify(query_temps=temp_dict)


if __name__=="__main__":
    app.run(debug=True)