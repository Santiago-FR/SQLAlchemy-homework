# Import dependencies
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Setup database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Create an app __name__
app = Flask(__name__)

# Dataframes/Queries
the_stations_df= pd.DataFrame(engine.execute('SELECT DISTINCT station FROM measurement').fetchall())
prcp_df = pd.DataFrame(session.query(Measurement.date,Measurement.station, Measurement.prcp,).all())
last_year_temps_df= pd.DataFrame(session.query(Measurement.date,Measurement.tobs).filter(Measurement.date <= '2017-08-23').filter(Measurement.date >= '2016-08-23').all())
all_tmps_df = pd.DataFrame(session.query(Measurement.date,Measurement.tobs).all())

# Dictionaries/Lists
prcp_dict = {}
stn_dict = {"station":[]}
last_year_temps_ls = []
all_tmps_dict= {}

# Loops
for i in range(len(prcp_df["date"])):
    prcp_dict[prcp_df["date"][i]]=prcp_df["prcp"][i]

for i in range(len(the_stations_df[0])):
    stn_dict["station"].append(the_stations_df[0][i])

for i in range(len(last_year_temps_df["date"])):
    last_year_temps_ls.append(last_year_temps_df["tobs"][i])

for i in range(len(all_tmps_df["date"])):
    all_tmps_dict[all_tmps_df["date"][i]]=all_tmps_df["tobs"][i]

# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    prec = "Preciepatation data by date: /api/v1.0/precipitation" 
    stn = "List of stations: /api/v1.0/stations"
    tobs = "Temperatures last 12 months on record: /api/v1.0/tobs"
    start = "Temperatures search from date: /api/v1.0/<start>"
    end = "Temperatures search from/to dates: /api/v1.0/<start>/<end>"
    
    return f"Welcome to the Climate Home page!<br/>---------<br/>Here are your routes:<br/><ul><li>{stn}</li><li>{prec}</li><li>{tobs}</li><li>{start}</li><li>{end}</li></ul>"

# Define route /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")
    return  jsonify(prcp_dict)

# Define route /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")
    return  jsonify(stn_dict)

# Define route /api/v1.0/stations
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'temperature' page...")
    return  jsonify(last_year_temps_ls)


# Define route /api/v1.0/<start>
@app.route("/api/v1.0/start")
def startd():
    print("Server received request for 'start' page...")
    return  jsonify(all_tmps_dict)


# Define route /api/v1.0/<start>/<end>
# @app.route("/api/v1.0/<start>/<end>")
# def calc_temps(start,end):
#     return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start).filter(Measurement.date <= end).all()

if __name__ == "__main__":
    app.run(debug=True)