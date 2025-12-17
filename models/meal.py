from database import db
from datetime import datetime

class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    date_time = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    is_on_diet = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)