import os
import json

from flask import Flask, make_response
from flask_restful import Api
from flasgger import Swagger
from simplexml import dumps
from sqlalchemy import create_engine

from students import student_manager


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app, prefix='/api/v1/')
    swagger = Swagger(app, template_file='./swagger_api_docs/template.yml')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=create_engine(
            "postgresql+psycopg2://postgres:9360@localhost/postgres",
            echo=False),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing\
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @api.representation('application/xml')
    def output_xml(data, code, headers=None):
        """Makes a Flask response with a XML encoded body"""
        resp = make_response(dumps({'report': data}), code)
        resp.headers.extend(headers or {})
        return resp

    @api.representation('application/json')
    def output_json(data, code, headers=None):
        """Makes a Flask response with a JSON encoded body"""
        resp = make_response(json.dumps(data), code)
        resp.headers.extend(headers or {})
        return resp

    api.add_resource(student_manager.ApiGetGroupsByStudentsCount, 'group/')
    api.add_resource(student_manager.ApiCourse, 'course/')
    api.add_resource(student_manager.ApiFindStudentsByCourse,
                     'course/<course>/')
    api.add_resource(student_manager.ApiStudent, 'student/')

    import db
    db.init_app(app)

    return app
