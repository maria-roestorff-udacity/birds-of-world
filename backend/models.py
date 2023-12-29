import os
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()


'''
Habitat to Bird Relationship
many to many
'''
range = db.Table('range',
                 db.Column('habitat_id', db.Integer, db.ForeignKey(
                     'Habitats.id'), primary_key=True),
                 db.Column('bird_id', db.Integer, db.ForeignKey(
                     'Birds.id'), primary_key=True)
                 )

'''
Region
Have name, image and habitats (one-to-many)
'''


class Region(db.Model):
    __tablename__ = 'Regions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    image_link = db.Column(db.String(500))
    habitats = db.relationship(
        'Habitat', backref=db.backref('habitat_region', lazy=True))

    def __init__(self, name, image_link=""):
        self.name = name
        self.image_link = image_link

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_link': self.image_link}


'''
Habitat
Have name and region_id 
'''


class Habitat(db.Model):
    __tablename__ = 'Habitats'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    region_id = db.Column(db.Integer, db.ForeignKey(
        'Regions.id'), nullable=False)

    def __init__(self, name, region_id):
        self.name = name
        self.region_id = region_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'region_id': self.region_id}


'''
Bird
Have common_name, species, image and habitats
'''


class Bird(db.Model):
    __tablename__ = 'Birds'

    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String, nullable=False, unique=True)
    species = db.Column(db.String, nullable=False)
    image_link = db.Column(db.String(500))
    habitats = db.relationship('Habitat', secondary=range,
                               backref=db.backref('Birds', lazy=True))

    def __init__(self, common_name, species, image_link=""):
        self.common_name = common_name
        self.species = species
        self.image_link = image_link

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def edit_format(self):
        habitat_id = [item.id for item in self.habitats]
        return {
            'id': self.id,
            'common_name': self.common_name,
            'species': self.species,
            'image_link': self.image_link,
            'habitats': habitat_id}

    def format(self):
        habitats = [{'name': item.name, 'id': item.id}
                    for item in self.habitats]
        regions = []
        [regions.append(reg.habitat_region)
         for reg in self.habitats if reg.habitat_region not in regions]
        region_info = [{'name': item.name, 'image': item.image_link}
                       for item in regions]

        return {
            'id': self.id,
            'common_name': self.common_name,
            'species': self.species,
            'image_link': self.image_link,
            'habitats': habitats,
            'regions': region_info}
