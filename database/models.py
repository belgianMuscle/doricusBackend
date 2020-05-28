import os
import json
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
 
database_name = os.environ.get('DB_NAME', 'Doricus')
#database_path = "postgres://{}:{}@{}/{}".format('postgres', 'udacity','localhost:5432', database_name)
database_path = os.environ.get('DB_PATH', "postgres://{}:{}@{}/{}".format('postgres', 'udacity','localhost:5432', database_name))
       
db = SQLAlchemy()
 
#Uncomment following call only once
#setup_db(app)
#    binds a flask application and a SQLAlchemy service
 
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #db.create_all()
 
class Member(db.Model):  
  __tablename__ = 'members'
 
  id = Column(Integer, primary_key=True)
  auth0_id = Column(String)
  type = Column(String)
  category = Column(String)
  difficulty = Column(Integer)
 
  def __init__(self, auth0_id, type):
    self.auth0_id = auth0_id
    self.type = type
 
 
class Project(db.Model):  
  __tablename__ = 'projects'
 
  id = Column(Integer, primary_key=True)
  member_id = Column(Integer)
  title = Column(String)
  description = Column(String)
  start_date = Column(String)
  proj_end_date = Column(String)
  act_end_date = Column(String)
  address = Column(String)
 
  def __init__(self, member_id, title, description, start_date, proj_end_date, act_end_date, address):
    self.member_id = member_id
    self.title = title
    self.description = description
    self.start_date = start_date
    self.proj_end_date = proj_end_date
    self.act_end_date = act_end_date
    self.address = address
 
class ProjectMember(db.Model):  
  __tablename__ = 'project_members'
 
  id = Column(Integer, primary_key=True)
  project_id = Column(Integer)
  member_id = Column(Integer)
 
  def __init__(self, project_id, member_id):
      self.project_id = project_id
      self.member_id = member_id
 
class Topic(db.Model):  
  __tablename__ = 'topics'
 
  id = Column(Integer, primary_key=True)
  project_id = Column(Integer)
  member_id = Column(Integer)
  timestamp = Column(String)
  title = Column(String)
  type = Column(String)
  event_date = Column(String)
  content = Column(String)
  visibility = Column(String)
 
  def __init__(self, project_id, member_id, timestamp, title, type, event_date, content, visibility):
      self.project_id = project_id
      self.member_id = member_id
      self.timestamp = timestamp
      self.title = title
      self.type = type
      self.event_date = event_date
      self.content = content
      self.visibility = visibility
 
class TopicComment(db.Model):  
  __tablename__ = 'topic_comments'
 
  id = Column(Integer, primary_key=True)
  topic_id = Column(Integer)
  member_id = Column(Integer)
  timestamp = Column(String)
  content = Column(String)
 
  def __init__(self, topic_id, member_id, timestamp, content):
      self.topic_id = topic_id
      self.member_id = member_id
      self.timestamp = timestamp
      self.content = content