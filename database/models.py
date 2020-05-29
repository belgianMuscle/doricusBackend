import os
import json
import datetime
import dateutil
import babel
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy

database_name = os.environ.get('DB_NAME', 'Doricus')
database_path = os.environ.get('DB_PATH', "postgres://{}:{}@{}/{}".format(
    'postgres', 'udacity', 'localhost:5432', database_name))

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


def getCurrentTime():
    return datetime.datetime.now()

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    elif format == 'short':
        format = "EE MM, dd, y"
    return babel.dates.format_datetime(date, format)


class Member(db.Model):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    auth0_id = Column(String, nullable=False)
    type = Column(String)
    projects = db.relationship('members', lazy=True, cascade="all", backref='member')

    def __init__(self, auth0_id, type=""):
        self.auth0_id = auth0_id
        self.type = type

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'auth0_id': self.auth0_id,
            'type': self.type
        }

    def long(self):
        return {
            'id': self.id,
            'auth0_id': self.auth0_id,
            'type': self.type
        }

    def __repr__(self):
        return json.dumps(self.short())


class Project(db.Model):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, db.ForeignKey('members.id'), nullable=False)
    title = Column(String)
    description = Column(String)
    start_date = Column(DateTime)
    proj_end_date = Column(DateTime)
    act_end_date = Column(DateTime)
    address = Column(String)
    members = db.relationship('members', lazy=True, cascade="all", backref='project')
    topics = db.relationship('topics', lazy=True, cascade="all, delete-orphan", backref='project')

    def __init__(self, member_id, title="", description="", start_date=getCurrentTime(), proj_end_date, act_end_date, address=""):
        self.member_id = member_id
        self.title = title
        self.description = description
        self.start_date = start_date
        self.proj_end_date = proj_end_date
        self.act_end_date = act_end_date
        self.address = address

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'title': self.title,
            'description': self.description
        }

    def long(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date,
            'proj_end_date': self.proj_end_date,
            'act_end_date': self.act_end_date,
            'address': self.address
        }

    def __repr__(self):
        return json.dumps(self.short())


class ProjectMember(db.Model):
    __tablename__ = 'project_members'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, db.ForeignKey('projects.id'), nullable=False)
    member_id = Column(Integer, db.ForeignKey('members.id'), nullable=False)

    def __init__(self, project_id, member_id):
        self.project_id = project_id
        self.member_id = member_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'member_id': self.member_id
        }

    def long(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'member_id': self.member_id
        }

    def __repr__(self):
        return json.dumps(self.short())


class Topic(db.Model):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, db.ForeignKey('projects.id'), nullable=False)
    member_id = Column(Integer, db.ForeignKey('members.id'), nullable=False)
    timestamp = Column(DateTime)
    title = Column(String)
    type = Column(String)
    event_date = Column(DateTime)
    content = Column(String)
    visibility = Column(String)
    comments = db.relationship('topic_comments', lazy=True, cascade="all, delete-orphan", backref='topic')

    def __init__(self, project_id, member_id, timestamp=getCurrentTime(), title="", type="", event_date, content="", visibility="closed"):
        self.project_id = project_id
        self.member_id = member_id
        self.timestamp = timestamp
        self.title = title
        self.type = type
        self.event_date = event_date
        self.content = content
        self.visibility = visibility

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'member_id': self.member_id,
            'timestamp': self.timestamp,
            'title': self.title,
            'type': self.type,
            'event_date': self.event_date,
            'content': self.content,
            'visibility': self.content
        }

    def long(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'member_id': self.member_id,
            'timestamp': self.timestamp,
            'title': self.title,
            'type': self.type,
            'event_date': self.event_date,
            'content': self.content,
            'visibility': self.content
        }

    def __repr__(self):
        return json.dumps(self.short())


class TopicComment(db.Model):
    __tablename__ = 'topic_comments'

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, db.ForeignKey('topics.id'), nullable=False)
    member_id = Column(Integer, db.ForeignKey('members.id'), nullable=False)
    timestamp = Column(DateTime)
    content = Column(String)

    def __init__(self, topic_id, member_id, timestamp=getCurrentTime(), content=""):
        self.topic_id = topic_id
        self.member_id = member_id
        self.timestamp = timestamp
        self.content = content

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'topic_id': self.topic_id,
            'member_id': self.member_id,
            'timestamp': self.timestamp,
            'content': self.content
        }

    def long(self):
        return {
            'id': self.id,
            'topic_id': self.topic_id,
            'member_id': self.member_id,
            'timestamp': self.timestamp,
            'content': self.content
        }

    def __repr__(self):
        return json.dumps(self.short())
