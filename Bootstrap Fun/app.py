import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify, render_template
import datetime as dt



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Base.classes.keys()
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home_page():
    """List all available api routes."""
    
    return (render_template('base.html'))
        # f"Available Routes:<br/>"
        # f"/api/v1.0/precipitation<br/>"
        # f"/api/v1.0/stations<br/>"
        # f"/api/v1.0/tobs<br/>"
        # f"/api/v1.0/<start><br/>"
        # f"/api/v1.0/<start>/<end>"


@app.route("/api/v1.0/precipitation")
def precipitation():
    render_template('base.html')
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all date and precipitation values"""
    # Query all date and precipitation values
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()


    # Create a dictionary from the row data and append to a list of all_stations
    all_precip = []
    for date, precip in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = precip
        all_precip.append(precip_dict)
        
    # Convert list of tuples into normal list
    # all_precip = list(np.ravel(results))

    return jsonify(all_precip)


@app.route("/api/v1.0/stations")
def stations():
    render_template('base.html')
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()
    #or
    #results = engine("select name, age, sex from passenger")

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    # # Create a dictionary from the row data and append to a list of all_stations
    # all_stations = []
    # for id, station, name, latitude, longitude, elevation in results:
    #     station_dict = {}
    #     station_dict["id"] = id
    #     station_dict["station"] = station
    #     station_dict["name"] = name
    #     station_dict["latitude"] = latitude
    #     station_dict["longitude"] = longitude
    #     station_dict["elevation"] = elevation
    #     all_stations.append(station_dict)

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    render_template('base.html')
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    # start_date = dt.date(2017, 8, 22) + dt.timedelta(-((365 * 1) + 0))
    """Return a list of tobs"""
    results = session.query(Measurement.date, Measurement.tobs).all()
        # filter(Measurement.date > start_date).all()
        # filter(Measurement.tobs).all()
        # filter(Measurement.station == 'USC00519281').all()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))
    
    return jsonify(all_names)

# @app.route("/api/v1.0/<start>")
# def start(start_date):
#     render_template('base.html', start_date)
#     # Create our session (link) from Python to the DB
#     session = Session(engine)
    
#     start_date = '2012-02-28'
#     end_date = dt.date.today
    
    
#     # This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
#     # and return the minimum, average, and maximum temperatures for that range of dates
#     def calc_temps(start_date):
#         return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#             filter(Measurement.date >= start_date).all()

#     # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))
    
#     return jsonify(all_names)

# @app.route("/api/v1.0/<start>/<end>")
# def end(start_date, end_date):
#     render_template('base.html', start_date, end_date)
#     # Create our session (link) from Python to the DB
#     session = Session(engine)
    
#     start_date = '2012-02-28'
#     end_date = '2012-03-05'
#     # print(calc_temps(start_date, end_date))
    
#     # This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
#     # and return the minimum, average, and maximum temperatures for that range of dates
#     def calc_temps(start_date, end_date):
#         return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#             filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

#     # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))
    
#     return jsonify(all_names)



if __name__ == '__main__':
    app.run(debug=True, port=5010)
