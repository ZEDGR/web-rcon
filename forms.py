from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError


class LoginForm(FlaskForm):
    username = TextField("username", [DataRequired()])
    password = PasswordField("password", [DataRequired()])

    class Meta:
        csrf = False


class PlayerKickForm(FlaskForm):
    player_num = TextField("Player Number", [DataRequired()])

    def validate_player_num(form, field):
        if not field.data.isnumeric():
            raise ValidationError("Invalid Player ID")

    class Meta:
        csrf = False


class PlayerBanForm(FlaskForm):
    player_ip = TextField("Player IP", [DataRequired()])

    class Meta:
        csrf = False
