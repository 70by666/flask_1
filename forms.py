from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Invalid email address.")])
    password = PasswordField("Password: ", 
                             validators=[DataRequired(), 
                                         Length(min=3, 
                                                max=32, 
                                                message="Please lengthen this text to 6 characters or more")])
    save = BooleanField("Save", default=False)
    submit = SubmitField("Submit")
