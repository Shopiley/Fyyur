import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/fyyur'
SQLALCHEMY_DATABASE_URI = 'postgresql://hmazppnfepzjsb:73afc90bd46be50812a1d509a4611e8daf61e19bb3286978dbcdf7b846192bc3@ec2-34-199-68-114.compute-1.amazonaws.com:5432/d16b9ec5afq4af'
SQLALCHEMY_TRACK_MODIFICATIONS = 'False' 
