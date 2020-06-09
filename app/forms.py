from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, Length, Required
from app.models import User, Dataset
from flask_login import current_user, login_user, login_required, logout_user


class AdvancedInputForm(FlaskForm):
    command_line = StringField('Run instruction')
    provenance = StringField('Provenance')
    code_btw = StringField('Line of code to run between package install and  execute')
    sample_output = StringField('Sample output that you want to compare for')


class InputForm(FlaskForm):
    # doi = StringField('Harvard Dataverse DOI', validators=[Optional()])
    zip_file = FileField('Zip File Containing Dataset')
    set_file = FileField('or---A set of Data file and scripts', render_kw={'multiple': True})
    name = StringField('Name of the Dataset', validators=[DataRequired()])
    fix_code = BooleanField('Attempt to automatically fix code')
    extended_lib = BooleanField('Extended Library handling')

    language = SelectField('What language is included in your upload', validators=[Required()],
                         choices=[('0', 'R'), ('1', 'Python')])

    # clean_code = BooleanField('Attempt to automatically clean code')
    submit = SubmitField('Build Docker Image')

    def validate_set_file(self, zip_file):
        # make sure there's either a DOI or a .zip file upload
        # if (not self.doi.data) and (self.zip_file.data is None) and (self.set_file.data is None):
        if (self.zip_file.data is None) and (self.set_file.data is None):
            raise ValidationError('Either the 1)dataset DOI or 2)a .zip or 3)a set of files '
                                  'containing the dataset is required.')

    def validate_name(self, name):
        if " " in name.data or not name.data.islower():
            raise ValidationError('Name is not allowed to contain uppercase letter or space.\nTry: '
                                  + name.data.replace(" ", "").lower())
        dataset = Dataset.query.filter_by(user_id=current_user.id, name=name.data).first()
        if dataset is not None:
            raise ValidationError('You already have a dataset with that name. Please choose a different name.')


# class PyplaceForm(FlaskForm):
# 	py_doi = StringField('Harvard Dataverse DOI', validators=[Optional()])
# 	py_zip_file = FileField('or---Zip File Containing Dataset')
# 	py_set_file = FileField('or---Set of python scripts',render_kw={'multiple': True})
# 	py_cmd_line = StringField('Command line (if needed)')
# 	py_name = StringField('Name of the Dataset', validators=[DataRequired()])
# 	py_fix_code = BooleanField('Attempt to automatically fix code')
# 	py_submit = SubmitField('Build Docker Image')
# 	def validate_zip_file(self, zip_file):
# 	    if (not self.doi.data) and (self.zip_file.data is None):
# 	        raise ValidationError('Either the dataset DOI or a .zip containing the dataset is required.')
#
# 	def validate_name(self, name):
# 		dataset = Dataset.query.filter_by(user_id=current_user.id, name=name.data).first()
# 		if dataset is not None:
# 			raise ValidationError('You already have a dataset with that name. Please choose a different name.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('That username is taken. Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('An account was found with that email address. Please use a different email address.')