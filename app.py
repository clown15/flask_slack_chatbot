import os
from flask import Flask,render_template,redirect,session
from models import db,User
from api_v1 import api as api_v1
from forms import SignupForm,SigninForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.register_blueprint(api_v1,url_prefix='/api/v1')

@app.route('/',methods=['GET'])
def home():
    userid = session.get('userid',None)
    return render_template('home.html',userid=userid)

@app.route('/signin',methods=['GET','POST'])
def signin():
    form = SigninForm()

    if form.validate_on_submit():
        session['userid'] = form.data.get('userid')

        return redirect('/')
    
    return render_template('signin.html',form=form)

@app.route('/signup',methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User()
        user.userid = form.data.get('userid')
        user.password = form.data.get('password')

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

        return redirect('/signin')

    return render_template('signup.html',form=form)

@app.route('/signout',methods=['GET'])
def signout():
    session.pop('userid',None)
    return redirect('/')




basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir,'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+dbfile
# True로 설정하면 각 리퀘스트의 끝에 데이터베이스 변경사항을 자동 커밋(저장,반영)한다.
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
# DB변경 사항을 추적할지에 대한 변수로 추적을 위해서는 추가 메모리가 필요하며 추적이 필요없다면 false로 설정해야한다.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# -------- csrf 설정 ------------------
app.config['SECRET_KEY'] = 'sdnajkfnwejknvjkfda'

# csrf token 설정
# csrf = CSRFProtect()
# csrf.init_app(app)
# -------------------------------------
# db설정값 초기화
db.init_app(app)
db.app = app
# db 생성
db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)