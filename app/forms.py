from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange

class RegisterForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(), EqualTo('password', message='Les mots de passe doivent correspondre')
    ])
    submit = SubmitField("S'inscrire")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField("Se connecter")

from wtforms import SelectField, IntegerField

from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class DeviceSelectionForm(FlaskForm):
    device_type = SelectField('Type de périphérique', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantité', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Valider la sélection')

    def set_device_choices(self, devices):
        self.device_type.choices = [(device.id, device.name) for device in devices]

class CSRFOnlyForm(FlaskForm):
    pass
