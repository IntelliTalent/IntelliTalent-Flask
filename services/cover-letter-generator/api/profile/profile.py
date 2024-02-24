from flask import current_app as app
from sqlalchemy import Column, String, Integer, Text, Boolean, Date, JSON
from sqlalchemy.orm import relationship
from ..app import db

class AbstractEntity(db.Model):
    __abstract__ = True

    created_at = Column(Date, default=db.func.current_timestamp(), nullable=False)
    updated_at = Column(Date, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)
    deleted_at = Column(Date, nullable=True)

class Profile(AbstractEntity):
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False)
    job_title = Column(String, nullable=True)
    skills = Column(JSON, default=[])
    years_of_experience = Column(Integer, nullable=True)
    graduated_from_cs = Column(Boolean, nullable=True)
    languages = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    cv = Column(Text, nullable=True)
    linked_in = Column(Text, nullable=True)
    git_hub = Column(Text, nullable=True)

    experiences = relationship('Experience', back_populates='profile')
    educations = relationship('Education', back_populates='profile')
    projects = relationship('Project', back_populates='profile')
    certificates = relationship('Certificate', back_populates='profile')

class Experience(AbstractEntity):
    id = Column(Integer, primary_key=True)
    job_title = Column(String, nullable=False)
    company_name = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    description = Column(Text, nullable=False)

    profile_id = Column(String(36), db.ForeignKey('profile.id'))
    profile = relationship('Profile', back_populates='experiences')

class Education(AbstractEntity):
    id = Column(Integer, primary_key=True)
    degree = Column(Text, nullable=False)
    school_name = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    description = Column(Text, nullable=False)

    profile_id = Column(String(36), db.ForeignKey('profile.id'))
    profile = relationship('Profile', back_populates='educations')

class Project(AbstractEntity):
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    skills = Column(Text, nullable=False)

    profile_id = Column(String(36), db.ForeignKey('profile.id'))
    profile = relationship('Profile', back_populates='projects')

class Certificate(AbstractEntity):
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    authority = Column(Text, nullable=False)
    issued_at = Column(Date, nullable=False)
    valid_until = Column(Date, nullable=True)
    url = Column(Text, nullable=False)

    profile_id = Column(String(36), db.ForeignKey('profile.id'))
    profile = relationship('Profile', back_populates='certificates')
