from flask import Flask, jsonify


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
    return('all available routes here')



@app.route('/api/v1.0/precipitation')
def precipitation(): 
    return('This is the precipiation page')
# Convert the query results to a dictionary using date as the key and prcp as the value.

# Return the JSON representation of your dictionary.

@app.route('/api/v1.0/stations')
def stations():
# Return a JSON list of stations from the dataset.
    return('This is the stations page')


@app.route('/api/v1.0/tobs')
def tobs():
    return('This is the tobs page')
# # Query the dates and temperature observations 
# of the most active station for the last year of data.

# # Return a JSON list of temperature observations (TOBS) 
# for the previous year.



# @app.route
# /api/v1.0/<start> and /api/v1.0/<start>/<end>

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.


if __name__=="__main__":
    app.run(debug=True)