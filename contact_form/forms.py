from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=5, max=500)])
    attachment = FileField("Attachment")
    submit = SubmitField("Send Message")
