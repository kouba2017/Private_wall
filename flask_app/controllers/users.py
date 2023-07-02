from flask_app.models import user, message
from flask import render_template, redirect, request, flash,session
from flask_bcrypt import Bcrypt
from flask_app import app

bcrypt= Bcrypt(app)

@app.route('/')
def home():
    return render_template("index.html")

#-----------registration------
@app.route('/register', methods=["POST"])
def register():
    if user.User.validation(request.form):
        hashed_password = bcrypt.generate_password_hash(request.form['password'])
        user_data={
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': hashed_password
        }
        session['user_id']=user.User.save(user_data)
        print('user_id')
        return redirect('/main_page')
    else:
        print('invalid data')
        return redirect('/')
    
#-----login--------
@app.route('/login' , methods=['POST'])
def login():
    #validity of the email 
    user_exist= user.User.get_by_email({'email':request.form['email']})
    if user_exist:
        if not bcrypt.check_password_hash(user_exist.password,request.form['password']):
            flash('wrong inputs','login')
            return redirect('/')
        else:
            session['user_id']=user_exist.id
            return redirect('/main_page')
    else:
        flash('account does not exist',"login")
        return redirect('/')

@app.route('/main_page')
def main_page():
    if 'user_id'not in session:
        redirect('/')
    all_messages=message.Message.get_by_user_id({'id':session['user_id']})
    sent_messages=message.Message.get_by_contact_id({'id':session['user_id']})
    user_in= user.User.get_by_id({'id':session['user_id']})
    print(user_in)
    #print(user_in[1].id)
    all_users=user.User.get_all()
    return render_template("main.html",user_in=user_in,all_users=all_users,messages_sent=sent_messages, all_messages=all_messages, number_of_messages=len(all_messages))

#----logout------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')