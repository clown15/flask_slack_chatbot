from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Todo(db.Model):
    __talbename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(128))
    title = db.Column(db.String(256))
    tstamp = db.Column(db.DateTime,server_default=db.func.now())

    # 함수에 접근할때 변수처럼 사용가능
    @property
    def serialize(self):
        return {
            'id':self.id,
            'title':self.title,
            'tstamp':self.tstamp
        }