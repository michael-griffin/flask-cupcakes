"""Forms for adopt app."""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Optional, URL


class AddCupcakeForm(FlaskForm):
    """Form for adding a cupcake"""
    flavor = StringField("Cupcake Flavor: ",
                         validators=[InputRequired()])

    size = StringField("Cupcake size: ",
                       validators=[InputRequired()])

    rating = IntegerField("Cupcake rating: ",
                        validators=[InputRequired()])

    image_url = StringField("Cupcake URL: ",
                            validators=[Optional(), URL()])



