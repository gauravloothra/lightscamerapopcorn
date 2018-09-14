from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
from flask_sqlalchemy import SQLAlchemy
engine = create_engine('sqlite:///login.db', echo=True)



app = Flask(__name__ , static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
db = SQLAlchemy(app)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login2.html')
    else:
        return render_template('home.html')
        #"Hello Boss!  <a href='/logout'>Logout</a>"

@app.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
        return render_template('signup2.html')
    return home()
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/signup", methods=['GET','POST'])
def signup():
    """Register Form"""
    if request.method == 'POST':
        new_user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('login2.html')
    return render_template('signup2.html')

@app.route("/bookseats" , methods=['GET','POST'])
def bookseats():
    if request.method == 'POST':
        city = request.form['cities']
        theatre = request.form['theatres_list']
        movie = request.form['movies_list']
        show = request.form['shows']
        return render_template('bookseats.html', city=city,theatre=theatre,movie=movie,show=show)



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)