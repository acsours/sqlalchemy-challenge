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
        f'Available api routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/station<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/temp/<br/>'
    )



@app.route('/api/v1.0/precipitation')
def precipitation(): 

    # return('This is the precipiation page')
# Convert the query results to a dictionary using date as the key and prcp as the value.
    session = Session(engine)
    # Query 12 months of data
    year_ago=dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    session.close()

    prcp_dict = {}
    for date, prcp in results:
        prcp_dict[date] = prcp
    
    # one line: 
    # precip = {date: prcp for date, prcp in precipitation}

# List of dictionaries method
    # all_measurements = []
    # for date, prcp in results:
    #     prcp_dict = {}
    #     prcp_dict['date'] = date
    #     prcp_dict['prcp'] = prcp
    #     all_measurements.append(prcp_dict)
    # convert list of tuples into normal lists
    # year_prcp = list(np.ravel(results))

# Return the JSON representation of your dictionary.
    return jsonify(prcp_dict)


@app.route('/api/v1.0/stations')
def stations():
# Return a JSON list of stations from the dataset.
    session = Session(engine)

    results=session.query(Station.station).all()

    session.close()

    all_stations=list(np.ravel(results))
    return jsonify(stations=all_stations)

    # all_stations = []
    # for each_station in results:
    #     all_stations.append(each_station)

    # return jsonify(all_stations)


    # return('This is the stations page')


@app.route('/api/v1.0/tobs')
def tobs():
#     return('This is the tobs page')
# # # Query the dates and temperature observations 
    session = Session(engine)

    year_ago=dt.date(2017, 8, 23) - dt.timedelta(days=365)

    station_results=session.query(Measurement.tobs)\
                    .filter(Measurement.station=='USC00519281')\
                    .filter(Measurement.date >= year_ago).all()

    session.close()
# # of the most active station for the last year of data.

    station_measurements=list(np.ravel(station_results))
    
    return jsonify(temperature=station_measurements)

    # active_stations = []
    # for each_measurement in station_results:
    #     active_stations.append(each_measurement)

    # return jsonify(active_stations)
        # active_station_dict = {}
        # active_station_dict['']
# # # Return a JSON list of temperature observations (TOBS) 
# # for the previous year.



# @app.route
# /api/v1.0/<start> and /api/v1.0/<start>/<end>

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""
    session = Session(engine)
    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        # calculate TMIN, TAVG, TMAX for dates greater than start
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        # Unravel results into a 1D array and convert to a list
        # temps = list(np.ravel(results))
        # return jsonify(temps)
    else:
    # calculate TMIN, TAVG, TMAX with start and stop
        results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    # Unravel results into a 1D array and convert to a list
    
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.


if __name__=="__main__":
    app.run(debug=True)