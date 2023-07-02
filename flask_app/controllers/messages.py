from flask_app.models import user, message
from flask import render_template, redirect, request,session
from flask_app import app

@app.route('/message/create', methods=['POST'])
def send():
    if 'user_id' not in session:
        return redirect('/')
    data={
        'user_id':request.form['user_id'],
        'contact_id': request.form['contact_id'],
        'content':request.form['content'],
    }
    print(data)
    message.Message.save(data)
    return redirect('/main_page')
@app.route('/message/delete/<int:msg_id>')
def vanish(msg_id):
    message.Message.delete({'id':msg_id})
    return redirect('/main_page')




