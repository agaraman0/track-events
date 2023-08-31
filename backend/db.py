from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

tracking_plan_event_association = db.Table(
    'tracking_plan_event_association',
    db.Column('tracking_plan_id', db.Integer, db.ForeignKey('tracking_plans.id')),
    db.Column('event_name', db.String, db.ForeignKey('events.name'))
)


class TrackingPlan(db.Model):
    __tablename__ = 'tracking_plans'

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String)

    # Define the one-to-many relationship with Event
    events = db.relationship("Event", secondary=tracking_plan_event_association, back_populates="tracking_plans")

    def __init__(self, display_name):
        self.display_name = display_name

    def to_dict(self):
        return {
            'id': self.id,
            'display_name': self.display_name,
            'events': [event.to_dict() for event in self.events]
        }


class Event(db.Model):
    __tablename__ = 'events'

    name = db.Column(db.String, primary_key=True)
    description = db.Column(db.String)
    rules = db.Column(db.JSON)

    # Define the many-to-many relationship with TrackingPlan
    tracking_plans = db.relationship("TrackingPlan", secondary=tracking_plan_event_association, back_populates="events")

    def __init__(self, name, description, rules):
        self.name = name
        self.description = description
        self.rules = rules

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'rules': self.rules,
            'tracking_plans': [tracking_plan.id for tracking_plan in self.tracking_plans]
        }
