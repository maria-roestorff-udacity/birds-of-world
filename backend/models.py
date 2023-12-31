import os
from flask_sqlalchemy import SQLAlchemy

# ----------------------------------------------------------------------------#
# Database setup
# ----------------------------------------------------------------------------#
database_path = os.environ['DATABASE_URL']
if database_path.startswith('postgres://'):
    database_path = database_path.replace('postgres://', 'postgresql://', 1)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    '''setup_db(app) binds a flask application and a SQLAlchemy service'''
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        # db.drop_all()
        db.create_all()


def test_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()


# ----------------------------------------------------------------------------#
# Models
# ----------------------------------------------------------------------------#
'''Habitat to Bird is many to many Relationship'''
range = db.Table('range',
                 db.Column('habitat_id', db.Integer, db.ForeignKey(
                     'Habitats.id'), primary_key=True),
                 db.Column('bird_id', db.Integer, db.ForeignKey(
                     'Birds.id'), primary_key=True)
                 )


class Region(db.Model):
    '''Region have name, image and habitats (one-to-many)'''
    __tablename__ = 'Regions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    image_link = db.Column(db.String(500))
    habitats = db.relationship(
        'Habitat', backref=db.backref('habitat_region', lazy=True))

    def __init__(self, name, image_link=''):
        self.name = name
        self.image_link = image_link

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_link': self.image_link}


class Habitat(db.Model):
    '''Habitat have name and region_id'''
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


class Bird(db.Model):
    '''Bird have common_name, species, image and habitats'''
    __tablename__ = 'Birds'

    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String, nullable=False, unique=True)
    species = db.Column(db.String, nullable=False)
    image_link = db.Column(db.String(500))
    habitats = db.relationship('Habitat', secondary=range,
                               backref=db.backref('Birds', lazy=True))

    def __init__(self, common_name, species, image_link=''):
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

    # Formatting the data that is displayed when listing Birds
    def format(self):
        # formatting habitats
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
