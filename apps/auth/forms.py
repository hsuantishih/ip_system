from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# 登入表單
class LoginForm(FlaskForm):
    # 設定表單中的標籤和驗證器
    account = StringField("帳號", validators=[DataRequired()])
    password = PasswordField("密碼", validators=[DataRequired()])
    submit = SubmitField("登入")