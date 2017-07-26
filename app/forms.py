from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, IPAddress


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class DoxForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    age = IntegerField('Age')
    dob = DateField('Date of Birth')
    address = TextAreaField('First Line Address')
    address1 = TextAreaField('Second Line Address')
    citystate = StringField('City and State')
    zipcode = StringField('ZIP Code')
    ipaddress = StringField('IP Address', validators=[IPAddress()])

class GeoIPForm(FlaskForm):
    ip = StringField('IP Address', validators=[IPAddress()])
