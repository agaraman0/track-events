import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, make_response, jsonify, request
from flask_cors import CORS

from config import config
from tracking_plans.routes import tracking_plans
from events.routes import events
from db import db, TrackingPlan, Event
from constants import PATH_NOT_FOUND, SERVER_ERROR, FAILURE_RESPONSE

app = Flask(__name__)
CORS(app)

handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
# set the log level in the handler
handler.setLevel(logging.DEBUG)

# set up the formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handler to the logger
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)  # set level to DEBUG

app.config.from_object(config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
app.register_blueprint(tracking_plans)
app.register_blueprint(events)


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Hello World</h1>'''


@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify(FAILURE_RESPONSE), 400)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify(PATH_NOT_FOUND), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify(SERVER_ERROR), 500)


if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')
