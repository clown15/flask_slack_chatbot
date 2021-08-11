from models import User
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired,EqualTo

class SignupForm(FlaskForm):
    userid = StringField('userid',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired(),EqualTo('re_password',message='입력한 비밀번호가 다릅니다.')])
    re_password = PasswordField('re_password',validators=[DataRequired()])

class SigninForm(FlaskForm):
    class check_password(object):
        def __init__(self,message=None):
            self.message = message
        
        def __call__(self,form,field):
            userid = form['userid'].data
            password = field.data
            user = User.query.filter_by(userid=userid).first()

            if user.password != password:
                raise ValueError('비밀번호가 틀렸습니다.')

    userid = StringField('userid',validators=[DataRequired()],description="아이디")
    password = PasswordField('password',validators=[DataRequired(),check_password()],description="비밀번호")