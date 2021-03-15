from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_path= os.environ['DATABASE_URL']

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()



#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Movies(db.Model):
    __tablename__ = 'Movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(String)

    ##################################

    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': self.release_date
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


class Actors(db.Model):
    __tablename__ = 'Actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    
    ##################################

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
    
    def long(self):
        return {
            'id': self.id,
            'title': self.name,
            'recipe': self.gender
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.long())