from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, SelectMultipleField, HiddenField
from flask_pagedown.fields import PageDownField
from wtforms import validators

class LoginForm(FlaskForm):
    username = TextField('Username*', [validators.Required("Please enter \
      your name.")])
    password = PasswordField('Password*', [validators.Required("Please enter \
      your password.")])
    submit = SubmitField('Login')

class SignUpForm(FlaskForm):
    username = TextField('Username*', [validators.Required("Please enter \
      your username")])
    email = TextField('Email*', [validators.Required("Please enter \
      your email"), validators.Email('Email format incorrect')])
    password = PasswordField('Password*', [validators.Required("Please enter \
      your password"), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password*', [validators.Required("Confirm \
      your password")])
    submit = SubmitField('Signup')

class AddNoteForm(FlaskForm):
    note_id = HiddenField("Note ID:")
    note_title = TextField('Lecture Title:', [validators.Required("Please enter \
      a note title.")])
    note = PageDownField('Upload Audio File:')
    edit = PageDownField('Edit Transcript:')
    submit = SubmitField('Add to Library')

class AddNoteFormVideo(FlaskForm):
    note_id = HiddenField("Note ID:")
    note_title = TextField('Lecture Title:', [validators.Required("Please enter \
      a note title.")])
    note = PageDownField('Upload Video File:')
    edit = PageDownField('Edit Transcript:')
    submit = SubmitField('Add to Library')

class EmailForm(FlaskForm):
    email = TextField('Email:')
    translation = HiddenField('Translation:')
    submit = SubmitField('Send', [validators.Required("Please enter an email:")])

class ChangeEmailForm(FlaskForm):
    email = TextField('Email*', [validators.Required("Please enter \
      your email"), validators.Email('Email format incorrect')])
    submit = SubmitField('Update Email')

class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password*', [validators.Required("Please enter \
      your password"), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password*', [validators.Required("Confirm \
      your password")])
    submit = SubmitField('Update Password')
