import os
from flask import Flask
from models import db
from api_v1 import api as api_v1


app = Flask(__name__)
app.register_blueprint(api_v1,url_prefix='/api/v1')

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