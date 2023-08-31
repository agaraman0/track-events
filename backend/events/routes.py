from flask import jsonify, request, Blueprint

from db import Event, db

events = Blueprint("events", __name__, url_prefix="/events/v1")


# Create a new Event
@events.route('/', methods=['POST'])
def create_event():
    data = request.json
    try:
        name = data['name']
        description = data['description']
        rules = data['rules']
        new_event = Event(name=name, description=description, rules=rules)
        db.session.add(new_event)
        db.session.commit()
        return jsonify(message="Event created successfully"), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 400


# Retrieve an Event by ID
@events.route('/<string:event_name>', methods=['GET'])
def get_event(event_name):
    event = Event.query.filter_by(name=event_name).first()
    if event is None:
        return jsonify(message="Event not found"), 404
    return jsonify(event.to_dict()), 200


# Retrieve an Event by ID
@events.route('/<string:event_name>', methods=['PUT'])
def update_event(event_name):
    data = request.json
    event = Event.query.filter_by(name=event_name).first()
    if event is None:
        return jsonify(message="event not found"), 404
    try:
        event.name = data.get('name', event.name)
        event.description = data.get('description', event.description)
        event.rules = data.get('rules', event.rules)

        db.session.commit()
        return jsonify(message="event updated successfully"), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 400


@events.route('/<string:event_name>', methods=['DELETE'])
def delete_event(event_name):
    event = Event.query.filter_by(name=event_name).first()
    if event is None:
        return jsonify(message="Event not found"), 404

    try:
        db.session.delete(event)
        db.session.commit()
        return jsonify(message="Event deleted successfully"), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500


# List Tracking Plans Associated with an Event
@events.route('/<string:event_name>/tracking_plans', methods=['GET'])
def list_tracking_plans_for_event(event_name):
    event = Event.query.filter_by(name=event_name).first()
    if not event:
        return jsonify(message="Event not found"), 404

    tracking_plans = [tp.to_dict() for tp in event.tracking_plans]
    return jsonify(tracking_plans), 200
