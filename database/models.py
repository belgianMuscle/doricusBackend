import os
import json
import datetime
import dateutil
import babel
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy

database_name = os.environ.get('DB_NAME', 'Doricus')
database_path = os.environ.get('DATABASE_URL', "postgres://{}:{}@{}/{}".format(
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
    __tablename__ = 'Member'

    id = Column(Integer, primary_key=True)
    auth0_id = Column(String, nullable=False)
    type = Column(String)
    projects = db.relationship('Project', lazy=True, cascade="all", backref='member')

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
    __tablename__ = 'Project'

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, db.ForeignKey('Member.id'), nullable=False)
    title = Column(String)
    description = Column(String)
    start_date = Column(DateTime)
    proj_end_date = Column(DateTime)
    act_end_date = Column(DateTime)
    address = Column(String)
    members = db.relationship('Member', lazy=True, cascade="all", backref='project')
    topics = db.relationship('Topic', lazy=True, cascade="all, delete-orphan", backref='project')

    def __init__(self, member_id, title, description, start_date, proj_end_date, act_end_date, address):
        self.member_id = member_id
        self.title = title
        self.description = description
        self.start_date = start_date
        if not start_date:
              self.start_date = getCurrentTime()
        self.proj_end_date = proj_end_date
        self.act_end_date = act_end_date
        self.address = address

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def set_data(self, data):
        self.title = data.get('title')
        self.description = data.get('description')
        self.start_date = data.get('start_date')
        self.proj_end_date = data.get('proj_end_date')
        self.act_end_date = data.get('act_end_date')
        self.address = data.get('address')

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
    __tablename__ = 'ProjectMember'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, db.ForeignKey('Project.id'), nullable=False)
    member_id = Column(Integer, db.ForeignKey('Member.id'), nullable=False)

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
    __tablename__ = 'Topic'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, db.ForeignKey('Project.id'), nullable=False)
    member_id = Column(Integer, db.ForeignKey('Member.id'), nullable=False)
    timestamp = Column(DateTime)
    title = Column(String)
    type = Column(String)
    event_date = Column(DateTime)
    content = Column(String)
    visibility = Column(String)
    comments = db.relationship('TopicComment', lazy=True, cascade="all, delete-orphan", backref='topic')

    def __init__(self, project_id, member_id, timestamp, title, type, event_date, content, visibility):
        self.project_id = project_id
        self.member_id = member_id
        self.timestamp = timestamp
        if not timestamp:
              self.timestamp = getCurrentTime()
        self.title = title
        self.type = type
        self.event_date = event_date
        self.content = content
        self.visibility = visibility
        if not visibility:
              self.visibility = "closed"

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
    __tablename__ = 'TopicComment'

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, db.ForeignKey('Topic.id'), nullable=False)
    member_id = Column(Integer, db.ForeignKey('Member.id'), nullable=False)
    timestamp = Column(DateTime)
    content = Column(String)

    def __init__(self, topic_id, member_id, timestamp, content):
        self.topic_id = topic_id
        self.member_id = member_id
        self.timestamp = timestamp
        if not timestamp:
              self.timestamp = getCurrentTime()
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
