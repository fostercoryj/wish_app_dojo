from flask import Flask, render_template, request, redirect, flash, session
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
import re
app = Flask(__name__)
app.secret_key = "ifwisheswerehorses"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt= Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def registration():
    is_valid = True
    query = ('SELECT email FROM users')
    mysql = connectToMySQL('wish_app_db')
    email_unique = mysql.query_db(query)
    for email in email_unique:
        if request.form['email'] == email['email']:
            is_valid = False
            flash('Email already registered. Please log in.')
    if len(request.form['f_name'])<1:
        is_valid = False
        flash("Please enter a first name.")
    if len(request.form['l_name'])<1:
        is_valid = False
        flash('Please enter a last name.')
    if not EMAIL_REGEX.match(request.form['email']):   
        flash("Invalid email address.")
        is_valid = False
    if len(request.form['email'])<1:
        is_valid = False
        flash('Please enter an email address.')
    if len(request.form['pass'])<1:
        is_valid = False
        flash('Please enter a password.')
    if len(request.form['pass'])<8:
        is_valid = False
        flash('Please enter a password of 8 characters or more.')
    if request.form['pass'] != request.form['pass_c']:
        is_valid = False
        flash('Please check password confirmation.')
    if is_valid:
        flash("Validated")
        print("Validated")
        print(request.form)
        pw_hash = bcrypt.generate_password_hash(request.form['pass']) 
        print(pw_hash) 
        query = ("INSERT INTO users (first_name,last_name,email,password, created_at, updated_at) VALUES (%(f_name)s, %(l_name)s, %(email)s, %(password_hash)s,now(),now());")
        data = {
            'f_name': request.form['f_name'],
            'l_name': request.form['l_name'],
            'email':request.form['email'],
            'password_hash' : pw_hash
        }
        print(request.form)
        mysql = connectToMySQL('wish_app_db')
        reg_info = mysql.query_db(query,data)
        flash("Added to DB")
        print("Added to DB")
    return redirect("/")

@app.route('/login', methods =['POST'])
def login():
    query = ("SELECT * FROM users WHERE email = %(email)s;")
    data = {
        'email' : request.form['email']
    }
    mysql = connectToMySQL('wish_app_db')
    credentials = mysql.query_db(query, data)
    if credentials:
        if bcrypt.check_password_hash(credentials[0]['password'], request.form['password']):
            session['id'] = credentials[0]['id']
            session['name'] = credentials[0]['first_name']
            return redirect('/wishes')
        else:
            flash('Invalid Password')
            print('Check your Email & Password.')
            return redirect('/')
    else:
        flash('Please Try Again')
        return redirect('/')

@app.route('/wishes')
def wishes():
    if 'id' not in session:
        session.clear()
        return redirect('/')
    query3 = ("SELECT first_name FROM users WHERE users.id = %(id)s;")
    data3 = {
        'id' : session['id']
    }
    mysql3 = connectToMySQL('wish_app_db')
    namecall = mysql3.query_db(query3, data3)
    
    query = ("SELECT first_name, wish, wishes.created_at, wishes.id, granted FROM users LEFT JOIN wishes ON wishes.user_id = users.id WHERE users.id = %(id)s AND granted = false;")
    data = {
        'id' : session['id']
    }
    mysql = connectToMySQL('wish_app_db')
    wishes = mysql.query_db(query,data)
    query2 = ("SELECT first_name, wish, wishes.created_at, granted, granted_at, wishes.id FROM users LEFT JOIN wishes ON wishes.user_id = users.id  WHERE users.id = %(id)s and granted = true")
    data2 = {
        'id' : session['id']
    }
    mysql2 = connectToMySQL('wish_app_db')
    granted_wishes = mysql2.query_db(query2,data2)
    print (granted_wishes)
    return render_template('wishes.html', wishes = wishes, granted_wishes = granted_wishes, namecall = namecall)

@app.route('/wishes/new')
def make_wish():
    if 'id' not in session:
        session.clear()
        return redirect('/')
    return render_template('make_wish.html')

@app.route('/wishes/new/create', methods=['POST'])
def create_wish():
    if 'id' not in session:
        session.clear()
        return redirect('/')
    is_valid = True
    if len(request.form['new_wish']) < 3:
        flash('Please enter a more detailed wish.')
        is_valid = False

    if len(request.form['new_description']) < 3:
        flash('Please enter a more detailed description.')
        is_valid = False

    if is_valid:
        print('Form valid')
        query = ("INSERT INTO wishes (wish, description, granted, created_at, updated_at, user_id) VALUES (%(wish)s,%(description)s, false, now(), now(),%(id)s);")
        data = {
            'wish' : request.form['new_wish'],
            'description' : request.form['new_description'],
            'id' : session['id']
        }
        mysql = connectToMySQL('wish_app_db')
        new_wish = mysql.query_db(query,data)
        return redirect('/wishes')
    return redirect('/wishes/new')

@app.route('/wishes/edit/<int:wish_id>')
def edit_wish(wish_id):
    if 'id' not in session:
        session.clear()
        return redirect('/')
    mysql = connectToMySQL('wish_app_db')
    query = ('SELECT * FROM wishes WHERE id = %(id)s')
    data = {
        'id' : wish_id
    }
    edit_wish = mysql.query_db(query,data)
    return render_template('edit.html', wishes = edit_wish)

@app.route('/edit/submit/<int:wish_id>',methods=['POST'])
def submit_edit(wish_id):
    is_valid = True
    if len(request.form['edit_wish']) < 3:
        flash('Please enter a more detailed wish.')
        is_valid = False
    if len(request.form['edit_description']) < 3:
        flash('Please enter a more detailed description.')
        is_valid = False
    if is_valid == True:
        print('Valid updates')
        query = ("UPDATE wishes SET wish = %(edit_wish)s, description = %(edit_description)s WHERE wishes.id = %(id)s;")
        data = {
            'edit_wish' : request.form['edit_wish'],
            'edit_description' : request.form['edit_description'],
            'id' : wish_id
        }
        mysql = connectToMySQL('wish_app_db')
        submit_edit_wish = mysql.query_db(query,data)
        return redirect('/wishes')
    return redirect(f'/wishes/edit/{wish_id}')

@app.route('/granted/<int:wish_id>')
def granted(wish_id):
    if 'id' not in session:
        session.clear()
        return redirect('/')
    query = ("UPDATE wishes SET granted = true, granted_at = now() WHERE wishes.id = %(wish_id)s")
    data = {
        'wish_id' : wish_id
    }
    mysql = connectToMySQL('wish_app_db')
    grant_wish = mysql.query_db(query, data)
    return redirect('/wishes')

@app.route('/remove/<int:wish_id>')
def remove(wish_id):
    query = ("DELETE FROM wishes WHERE wishes.id = %(wish_id)s;")
    data = {
        'wish_id' : wish_id
    }
    mysql = connectToMySQL('wish_app_db')
    remove_wish = mysql.query_db(query,data)
    return redirect('/wishes')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)