from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class UpdateUserForm(FlaskForm):
    """Form for updating users."""

    username = StringField('Username')
    email = StringField('E-mail', validators=[Optional(), Email()])
    image_url = StringField('(Optional) Image URL')
    header_image_url = StringField('(Optional) Image Header URL')
    bio = TextAreaField('(Optional) Bio')
    password = PasswordField('Password', validators=[Length(min=6)])


class OnlyCsrfForm(FlaskForm):
    """For actions where we want CSRF protection, but don't need any fields.

    Currently used for our "delete" buttons, which make POST requests, and the
    logout button, which makes POST requests.
    """