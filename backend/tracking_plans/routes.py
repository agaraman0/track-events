from flask import jsonify, request, Blueprint

from db import TrackingPlan, Event, db

tracking_plans = Blueprint("tracking_plans", __name__, url_prefix="/tracking-plans/v1")


@tracking_plans.route('/', methods=['POST'])
def create_tracking_plan():
    data = request.json
    try:
        data = data.get('tracking_plan', {})
        display_name = data.get('display_name', None)
        rules_data = data.get('rules', {})
        events_data = rules_data.get('events', {})
        new_tracking_plan = TrackingPlan(display_name=display_name)
        db.session.add(new_tracking_plan)

        for event_data in events_data:
            name = event_data.get('name', '')
            description = event_data.get('description', '')
            rules = event_data.get('rules', {})
            new_event = Event(name=name, description=description, rules=rules)
            new_tracking_plan.events.append(new_event)

        db.session.commit()
        return jsonify(message="Tracking plan created successfully"), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 400


# Retrieve a Tracking Plan by ID
@tracking_plans.route('/<int:tracking_plan_id>', methods=['GET'])
def get_tracking_plan(tracking_plan_id):
    tracking_plan = TrackingPlan.query.get(tracking_plan_id)
    if tracking_plan is None:
        return jsonify(message="Tracking plan not found"), 404
    return jsonify(tracking_plan.to_dict()), 200


# Update a Tracking Plan by ID
@tracking_plans.route('/<int:tracking_plan_id>', methods=['PUT'])
def update_tracking_plan(tracking_plan_id):
    data = request.json
    tracking_plan = TrackingPlan.query.get(tracking_plan_id)
    if tracking_plan is None:
        return jsonify(message="Tracking plan not found"), 404

    try:
        tracking_plan.display_name = data.get('display_name', tracking_plan.display_name)
        events_data = data.get('events', [])

        for event_data in events_data:
            event_name = event_data.get('name')
            if event_name:
                event = Event.query.get(name=event_name)
                if event:
                    event.description = event_data.get('description', event.description)
                    event.rules = event_data.get('rules', event.rules)

        db.session.commit()
        return jsonify(message="Tracking plan updated successfully"), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 400


@tracking_plans.route('/<int:tracking_plan_id>', methods=['DELETE'])
def delete_tracking_plan(tracking_plan_id):
    tracking_plan = TrackingPlan.query.get(tracking_plan_id)
    if tracking_plan is None:
        return jsonify(message="Tracking plan not found"), 404

    try:
        db.session.delete(tracking_plan)
        db.session.commit()
        return jsonify(message="Tracking plan deleted successfully"), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500


@tracking_plans.route('/<int:tracking_plan_id>/associate_events/<path:events>', methods=['POST'])
def associate_event_with_tracking_plan(tracking_plan_id, events):
    events = events.split(',')
    tracking_plan = TrackingPlan.query.get(tracking_plan_id)
    events = Event.query.filter(Event.name.in_(events)).all()

    if not tracking_plan or not events:
        return jsonify(message="Tracking plan or event not found"), 404

    tracking_plan.events.extend(events)
    db.session.commit()
    return jsonify(message="Event associated with tracking plan successfully"), 200


@tracking_plans.route('/', methods=['GET'])
def list_tracking_plans():
    tracking_plans = TrackingPlan.query.all()
    return jsonify([tp.to_dict() for tp in tracking_plans]), 200
