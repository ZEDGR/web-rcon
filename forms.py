from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms import PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError
from wtforms.validators import IPAddress


class LoginForm(FlaskForm):
    username = TextField("username", [DataRequired()])
    password = PasswordField("password", [DataRequired()])

    class Meta:
        csrf = False


class PlayerKickForm(FlaskForm):
    num = TextField("Player Number", [DataRequired()])

    def validate_player_num(form, field):
        if not field.data.isnumeric():
            raise ValidationError("Invalid Player ID")

    class Meta:
        csrf = False


class PlayerBanForm(FlaskForm):
    address = TextField("address", [DataRequired(), IPAddress()])
    name = TextField("name", [DataRequired()])
    num = TextField("num", [DataRequired()])

    class Meta:
        csrf = False
