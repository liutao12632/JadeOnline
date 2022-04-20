from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from app.models import User, Role

usernameRegex = '^[a-zA-Z][a-zA-Z0-9.—_()]*$'
passwordRegex = '^.{8,64}$'


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 64),
                                               Regexp(passwordRegex, 0, '密码至少需要八位')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64),
                                              Regexp(usernameRegex, 0, '用户名只可使用数字、字母、下划线、英文括弧英文句号并且要以字母开头')])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 64),
                                               Regexp(passwordRegex, 0, '密码至少需要八位')])
    password_confirm = PasswordField('再次输入密码', validators=[DataRequired(), EqualTo('password', '两次输入的密码必须一致')])
    address = StringField('送货地址', validators=[DataRequired()])
    about_me = TextAreaField('个人介绍')
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已经被注册.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已经被注册')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired(), Length(1, 64),
                                                    Regexp(passwordRegex, 0, '密码至少需要8位')])
    new_password = PasswordField('新密码', validators=[DataRequired(), Length(1, 64),
                                                    Regexp(passwordRegex, 0, '密码至少需要8位')])
    password_confirm = PasswordField('再次输入密码', validators=[DataRequired(), EqualTo('新密码', '密码必须一致')])
    submit = SubmitField('更改密码')


class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64),
                                              Regexp(usernameRegex, 0, '用户名只可使用数字、字母、下划线、英文括弧英文句号并且要以字母开头')])
    address = StringField('送货地址', validators=[DataRequired()])
    about_me = TextAreaField('个人介绍')
    submit = SubmitField('修改')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已经被注册')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64),
                                              Regexp(usernameRegex, 0, '用户名只可使用数字、字母、‘.’并且要以字母开头')])
    role = SelectField('角色', coerce=int)
    address = StringField('送货地址', validators=[DataRequired()])
    about_me = TextAreaField('个人介绍')
    submit = SubmitField('修改')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                            for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.email.data and User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已经被注册')

    def validate_username(self, field):
        if field.data != self.username.data and User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已经被注册')
