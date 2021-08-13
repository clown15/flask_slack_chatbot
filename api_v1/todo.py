from flask import jsonify
from flask import request,session
from models import Todo,db,User
import requests
import datetime
from . import api

def send_slack(msg):
    # slack주소로 api요청
    res = requests.post('https://hooks.slack.com/services/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', json = {
            'text': msg
        }, headers = {'Context-Type':'application/json'})
    print(res)
    return res

@api.route('/todos',methods=['GET','POST','PUT','DELETE'])
def todos():
    userid = session.get('userid',None)
    if not userid:
        return jsonify({'error':'로그인이 필요합니다.'}), 401

    if request.method == 'POST': 
        data = request.get_json()
        todo = Todo()
        todo.user_id = userid
        todo.title = data.get('title')
        todo.status = 0
        todo.due = data.get('date')

        db.session.add(todo)
        db.session.commit()

        send_slack("TODO가 생성되었습니다.")
        return jsonify(), 201

    elif request.method == 'PUT':
        data = request.get_json()
        todo_id = data.get("todo_id")
        todo = Todo.query.filter_by(id=todo_id,user_id=userid).first()
        if not todo:
            return jsonify({'error':'잘못된 요청입니다.'}), 404
        if todo.status:
            todo.status = 0
        else:
            todo.status = 1

        db.session.commit()
        send_slack("TODO가 완료되었습니다.")
        return jsonify(), 201

    elif request.method == 'GET':
        todos = Todo.query.filter_by(user_id==userid).all()
        # models.py 에 있는 serialize사용
        return jsonify([t.serialize for t in todos])
    
    elif request.method =='DELETE':
        data = request.get_json()
        todo_id = data.get("todo_id")
        todo = Todo.query.filter_by(id=todo_id,user_id=userid).first()
        if not todo:
            return jsonify({'error':'잘못된 요청입니다.'}), 404

        db.session.delete(todo)
        db.session.commit()
        send_slack("TODO가 삭제되었습니다.")
        return jsonify(), 204

    return jsonify({'error':'잘못된 요청입니다.'}), 404

@api.route('/slack/todos',methods=['POST'])
def slack():
    res = request.form['text'].split(' ',2)
    user = request.form['user_name']
    user_id = User.query.filter_by(slack_name=user).first().userid
    action, *args = res
    msg = ''

    if action == 'create':
        try:
            todo_name = args[1]
            todo = Todo()
            todo.user_id = user_id
            todo.title = todo_name
            todo.due = args[0]

            db.session.add(todo)
            db.session.commit()
            # msg = user+'님 todo가 생성되었습니다.'
            msg = '[%s] %s'%(str(args[0]),todo_name)
        except IndexError:
            msg = '잘못된 입력입니다.\n 입력된값 {%s}\n /flasktodo help'%(res)
    elif action == 'list':
        todos = Todo.query.filter(Todo.user_id==user_id).all()
        for index,todo in enumerate(todos):
            msg += '%d, %s (~%s)\n'%(todo.id,todo.title,str(todo.due))
    elif action == 'done':
        todo_id = args[0]
        todo = Todo.query.filter_by(id=todo_id,user_id=user_id).first()
        if todo:
            todo.status = 1
            db.session.commit()

            msg = '%s 완료되었습니다.'%(todo.title)
        else:
            msg = "잘못된 입력입니다.\n /flasktodo help"

    elif action == 'delete':
        todo_id = args[0]
        todo = Todo.query.filter_by(id=todo_id,user_id=user_id).first()
        if todo:
            msg = "%s 삭제되었습니다."%(todo.title)
            db.session.delete(todo)
            db.session.commit()
        else:
            msg = "잘못된 입력입니다.\n /flasktodo help"

    elif action == 'help':
        msg += '생성:create MM/DD/YYYY todo_title\n'
        msg += '확인:list\n'
        msg += '완료:done todo_id\n'
        msg += '삭제:delete todo_id'

    else:
        msg = '잘못된 입력입니다.\n'
        msg += '생성:create MM/DD/YYYY todo_title\n'
        msg += '확인:list\n'
        msg += '완료:done todo_id\n'
        msg += '삭제:delete todo_id'

    return msg