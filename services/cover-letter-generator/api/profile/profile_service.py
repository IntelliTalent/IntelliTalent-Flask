from .profile import Profile
from ..app import db
from flask import current_app as app

def create_profile(fullname):
    new_profile = Profile(fullname=fullname)
    db.session.add(new_profile)
    db.session.commit()
    return new_profile.as_dict()

def get_all_profiles():
    profiles = Profile.query.all()
    
    profiles_as_dict = [profile.as_dict() for profile in profiles]
    
    return profiles_as_dict
