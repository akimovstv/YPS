from flask import Flask
from flask_restful import Api

from db import database
from resources.catalogue import Catalogue
from resources.course import ExistedCourse, NewCourse

# Create Flask and API objects.
app = Flask(__name__)
api = Api(app)


# Create database before first request
@app.before_first_request
def setup_db():
    database.create_tables()


# Register api endpoints.
api.add_resource(Catalogue, '/catalogue')
api.add_resource(NewCourse, '/course')
api.add_resource(ExistedCourse, '/course/<int:course_id>')
