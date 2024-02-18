from flask import current_app as app
from ..app import db
 
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}