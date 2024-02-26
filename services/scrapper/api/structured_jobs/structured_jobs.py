from sqlalchemy import Column, Date, JSON, Enum
from datetime import datetime
from ..app import db

class AbstractEntity(db.Model):
    __abstract__ = True

    created_at = Column(Date, default=db.func.current_timestamp(), nullable=False)
    updated_at = Column(Date, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)
    deleted_at = Column(Date, nullable=True)

class StructuredJob(AbstractEntity):
    __tablename__ = 'structured_job'

    id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    company = db.Column(db.String, nullable=False)
    job_location = db.Column(db.String, nullable=False)
    type = db.Column(Enum("Full Time", "Part Time", "Contract", "Internship", "Temporary", "Volunteer", "Other"), nullable=False)
    skills = db.Column(JSON, default=[])
    url = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    published_at = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    job_place = db.Column(Enum("Remote", "On Site", "Hybrid"), nullable=False)
    needed_experience = db.Column(db.Integer, nullable=True)
    education = db.Column(db.String, nullable=True)
    cs_required = db.Column(db.Boolean, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_scrapped = db.Column(db.Boolean, default=False, nullable=False)
    custom_filters = db.Column(JSON, nullable=True)
    interview_questions = db.Column(db.ARRAY(db.String), nullable=True)
