from wtforms import BooleanField, StringField,IntegerField,DecimalField, PasswordField,FloatField,SubmitField,SelectField,validators,TextAreaField
from wtforms.fields import MultipleFileField
from wtforms.fields.html5 import TimeField
from wtforms.widgets import TextArea
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired,FileAllowed
from flask_uploads import configure_uploads,IMAGES,UploadSet,patch_request_class
from PIL import Image,ImageGrab
##from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import os
from flask_session import Session
from flask import Flask,render_template,send_from_directory,request,redirect,flash,url_for,session

##app = Flask(__name__)
##app.config['SESSION_TYPE'] = 'filesystem'
##app.config['SECRET_KEY'] = os.urandom(24)
##app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
##
##images = UploadSet('photos',IMAGES)
##configure_uploads(app,images)
##patch_request_class(app)
##
##Session(app)
####POSTGRES = {
####    'user':'dominicsham807',
####    'pw':'996322',
####    'db':'food_delivery',
####    'host':'127.0.0.1',
####    'port':'5432',
####}
##UPLOAD_FOLDER = 'static/images'
##ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
##app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
##app.config['MYSQL_HOST'] = 'localhost'
##app.config['MYSQL_USER'] = 'root'
##app.config['MYSQL_PASSWORD'] = 'Ds996322'
##app.config['MYSQL_DB'] = 'food_delivery'
##
##mysql = MySQL(app)

class CustomerRegister(FlaskForm):
    name = StringField('Name',[validators.Length(max=50)])
    mobile = IntegerField('Mobile', [validators.NumberRange(min=8)])
    email = StringField('Email',[validators.Length(max=200)])
    username = StringField('Username',[validators.Length(min=6,max=100)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm_pw',message='Enter a correct password!')
    ])
    confirm_pw = PasswordField('Confirm Password')
    member = BooleanField('Apply as member?', validators=[validators.AnyOf([True, False])])
    submit = SubmitField('Register')
                                
    
class LoginForms(FlaskForm):
    username = StringField('Username',[validators.Length(min=6,max=100)])
    password = PasswordField('Password',[validators.DataRequired("Please enter a password.")])

class StaffForm(FlaskForm):
    name = StringField('Name',[validators.Length(max=50)])
    username = StringField('Username',[validators.Length(min=6,max=100)])
    password = PasswordField('Password',[validators.DataRequired()])
    staff_id = IntegerField('ID number',[validators.NumberRange(min=8)])
    mobile = IntegerField('Mobile Number',[validators.NumberRange(min=8)])
    email = StringField('Email',[validators.Length(max=200)])
    submit = SubmitField('Add')

class Products(FlaskForm):
##    query = 'SELECT * FROM restaurants'
##    cursor.execute(query)
##    restaurants = cursor.fetchall()
    item = StringField('Item',[validators.Length(max=100)])
    cuisine_type = SelectField(
            label = 'Cuisines',
            validators=[validators.DataRequired('Please select one')],
            choices = [('Singapore Hainanese Chicken','Singapore Hainanese Chicken'),('Japanese Sushi','Japanese Sushi'),('Western Food','Western Food'),
                       ('Chinese Dim Sum','Chinese Dim Sum'),('Chinese Cuisines','Chinese Cuisines'),('Italian Pizza','Italian Pizza'),('American Fast Food','American Fast Food')],
    )

    restaurant = StringField('Restaurant',[validators.Length(max=200)])
    price = DecimalField('Price per unit', validators=[validators.Optional()], places=1)
    image = FileField('Image',validators=[FileRequired()])
    submit = SubmitField('Add')

class Restaurants(FlaskForm):
    name = StringField('Restaurant',[validators.Length(max=60)])
    cuisine_type = SelectField(
            label = 'Cuisines',
            validators=[validators.DataRequired('Please select one')],
            choices = [('Singapore Hainanese Chicken','Singapore Hainanese Chicken'),('Japanese Sushi','Japanese Sushi'),('Western Food','Western Food'),
                       ('Chinese Dim Sum','Chinese Dim Sum'),('Chinese Cuisines','Chinese Cuisines'),('Italian Pizza','Italian Pizza'),('American Fast Food','American Fast Food')],
    )
    address = StringField('Location',widget=TextArea())
    open_time = TimeField('Open at',format='%H:%M')
    close_time = TimeField('Close at',format='%H:%M')
    tel = IntegerField('Telephone', [validators.NumberRange(min=8)])
    hotline = IntegerField('Hotline', [validators.NumberRange(min=8)])
    submit = SubmitField('Add')


    
