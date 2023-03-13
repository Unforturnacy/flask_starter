from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from flask_wtf.file import FileRequired, FileAllowed

class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    no_bedroom = db.Column(db.Text)
    no_bathroom = db.Column(db.Text)
    location = db.Column(db.Text)
    price = db.Column(db.Text)
    type = db.Column(db.Text)
    photo = db.Column(db.Text)

    def __init__(self, title, description, no_bedroom, no_bathroom, location, price, type, photo):
        self.title = title
        self.description = description
        self.no_bedroom = no_bedroom
        self.no_bathroom = no_bathroom
        self.location = location
        self.price = price
        self.type = type
        self.photo = photo       

    def get_id(self):
        try:
            return unicodedata(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support 

class PropertyForm(FlaskForm):
    title = TextAreaField('Property Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    no_bedroom = TextAreaField('No. of Bedrooms', validators=[DataRequired()])
    no_bathroom = TextAreaField('No. of Bathrooms', validators=[DataRequired()])
    location = TextAreaField('Location', validators=[DataRequired()])
    price = TextAreaField('Price', validators=[DataRequired()])
    type = SelectField('Type', choices=[('House', 'House'), ('Apartment', 'Apartment')])
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])


