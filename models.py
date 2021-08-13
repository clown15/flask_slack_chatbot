from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Todo(db.Model):
    __talbename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128),db.ForeignKey('user.id'),nullable=False)
    title = db.Column(db.String(256))
    # 1:완료 , 0: 미완료
    status = db.Column(db.Integer)
    due = db.Column(db.String(64))
    tstamp = db.Column(db.Date,server_default=db.func.current_date())

    # 함수에 접근할때 변수처럼 사용가능
    @property
    def serialize(self):
        return {
            'id':self.id,
            'user':self.user.id,
            'title':self.title,
            'tstamp':self.tstamp
        }

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32),nullable=False,unique=True)
    slack_name = db.Column(db.String(32))
    password = db.Column(db.String(128),nullable=False)
    todos = db.relationship('Todo',backref='user',lazy=True)
