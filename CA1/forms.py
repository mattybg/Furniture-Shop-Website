from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, FloatField, FileField
from wtforms.validators import InputRequired, EqualTo, NumberRange
class RegistrationForm(FlaskForm):

    user_id = StringField("User id:",
        validators=[InputRequired()])
    password = PasswordField("Password:",
        validators=[InputRequired()])
    password2 = PasswordField("Repeat password:",
        validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user_id = StringField("User id:",
        validators=[InputRequired()])
    password=PasswordField("Password:",
        validators=[InputRequired()])
    submit = SubmitField("Submit")

class SortForm(FlaskForm):
    sort_by = SelectField("Sort By", choices=[("asc", "Price: Low to High"), ("desc", "Price: High to Low"), ("none", "Most Popular")],default="none", validators=[InputRequired()])
    submit = SubmitField('Sort')

class ProductForm(FlaskForm):
    name = StringField("Product Name:", validators=[InputRequired()])
    price = FloatField("Price:", validators=[InputRequired()])
    description = StringField("Product Description:", validators=[InputRequired()])
    image = FileField("Product Image:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class DeleteForm(FlaskForm):
    name = SelectField("Product Name:", validators=[InputRequired()])
