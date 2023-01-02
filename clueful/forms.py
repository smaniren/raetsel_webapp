import email
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator
from flask_login import current_user
from clueful.models import User
from clueful import bcrypt, app

class SignupForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(),Length(min=2, max=20)])
    email = StringField('Email', 
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Signup')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()        
        if user:
            raise ValidationError('The chosen username is already taken')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()        
        if user:
            raise ValidationError('There is already a clueful-account registered under this email-address')
    
      
        
    
class LoginForm(FlaskForm):
    email = StringField('Email', 
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    submit = SubmitField('Login')
    
    
class EditFormUsername(FlaskForm):
    username = StringField('Username',
                            validators=[Length(min=2, max=20)])
    submitUsername = SubmitField('ok!')    
    def validate_username(self, username):
        if username.data != current_user.username:          
            user = User.query.filter_by(username=username.data).first()        
            if user:
                raise ValidationError('The chosen username is already taken')
    
class EditFormEmail(FlaskForm):
    email = StringField('Email', 
                            validators=[Email()])
    submitEmail = SubmitField('ok!')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()        
            if user:
                raise ValidationError('There is already a clueful-account registered under this email-address')

class EditFormPassword(FlaskForm):
    current_password = PasswordField('Current Password',
                            validators=[DataRequired()])
    password = PasswordField('New password',
                            validators=[DataRequired()])
    password_confirm = PasswordField('Confirm new password',
                            validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submitPassword = SubmitField('edit password!')
    
    def validate_current_password(self, current_password):
        if not bcrypt.check_password_hash(current_user.password,current_password.data):
            raise ValidationError('Password incorrect')
        
class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', 
                            validators=[DataRequired(), Email()])  
    submit = SubmitField('change password')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        print(user)      
        if not user:
            raise ValidationError('The email address you entered is not in use. Please sign up.')
        
class NewPasswordForm(FlaskForm):
    password = PasswordField('Password',
                            validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submitPassword = SubmitField('edit password!')
    
class SqlForm(FlaskForm):
    id = IntegerField('ID',
                            validators=[DataRequired()])
    column = SelectField('Column')
    value = TextAreaField('Value',
                            validators=[DataRequired()])
    """ type = RadioField('Type', 
                            choices=[('str', 'str'), ('int', 'int'), ('float', 'float')],
                            validators=[DataRequired()]) """
    password = PasswordField('Password',
                            validators=[DataRequired()])
    def validate_password(self,password):
        if password.data != app.config['SQL_PASSWORD']:
            raise ValidationError('Password incorrect')
    