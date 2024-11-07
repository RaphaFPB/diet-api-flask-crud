from database import db
from sqlalchemy import func

class Meal(db.Model):
    #id (int), Nome(txt), Descrição(txt), Data e hora(?), pode? (bool)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    description = db.Column(db.String(80), nullable = False)
    datetime = db.Column(db.DateTime, nullable = False, default=func.now())
    in_diet = db.Column(db.String(3), nullable = False)