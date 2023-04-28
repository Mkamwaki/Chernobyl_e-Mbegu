from app import db, admin
from datetime import datetime
from flask_admin.contrib.sqla import ModelView

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(), nullable = False)
    phone  = db.Column(db.String(), nullable = False, unique=True)
    password = db.Column(db.String(), nullable = False)
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    role = db.Column(db.Integer, unique=False, default=2) # 1 for admin, 2 for farmer
    ward_id = db.Column(db.Integer, db.ForeignKey('ward.id'), nullable=False)

    # relationship with activity table
    actions = db.relationship('Activity', backref='user', lazy=True)

    def __repr__(self):
        return '<user %r>' %self.fullname

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    action = db.Column(db.String(), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return '<activity %r>' %self.action

class Seed(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), unique=False, nullable=False)
  number = db.Column(db.String(), unique=False, nullable=False)
  description = db.Column(db.String(), unique=False, nullable=False)
  expire_date = db.Column(db.DateTime, nullable=False)
  manufucturer = db.Column(db.String(), unique=False, nullable=False)

  def __repr__(self) -> str:
        return '<seed %r>' %self.name

class Region(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), unique=False, nullable=False)

  # relationship with Ward table
  wards = db.relationship('Ward', backref='region', lazy=True)

  def __repr__(self) -> str:
        return '<region %r>' %self.name

class Ward(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), unique=False, nullable=False)
  region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)

  # relationship with User table
  users = db.relationship('User', backref='ward', lazy=True)

  def __repr__(self) -> str:
        return '<ward %r>' %self.name

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Activity, db.session))
admin.add_view(ModelView(Seed, db.session))
admin.add_view(ModelView(Region, db.session))
admin.add_view(ModelView(Ward, db.session))