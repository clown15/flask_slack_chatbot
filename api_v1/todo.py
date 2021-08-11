from flask import jsonify
from flask import request
from models import Todo,db
import requests
import datetime
from . import api

def send_slack(msg):
    # slack주소로 api요청
    res = requests.post('https://hooks.slack.com/services/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', json = {
            'text': msg
        }, headers = {'Context-Type':'application/json'})
    
    return res

@api.route('/todos',methods=['GET','POST'])
def todos():
    if request.method == 'POST':
        send_slack("TODO가 생성되었습니다.")
        
    elif request.method == 'GET':
        print(send_slack("TODO가 생성되었습니다."))
        

    data = request.get_json()
    return jsonify(data)

@api.route('/slack/todos',methods=['POST'])
def slack():
    res = request.form['text'].split(' ',1)
    user = request.form['user_name']
    action, *args = res
    msg = ''

    if action == 'create':
        todo_name = args[0]

        todo = Todo()
        todo.user = user
        todo.title = todo_name

        db.session.add(todo)
        db.session.commit()
        # msg = user+'님 todo가 생성되었습니다.'
        msg = '[%s] %s'%(str(datetime.datetime.now()),todo_name)
    elif action == 'list':
        todos = Todo.query.filter(Todo.user==user).all()
        for index,todo in enumerate(todos):
            msg += '%d, %s (~%s)\n'%(todo.id,todo.title,str(todo.tstamp))
    return msg