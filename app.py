from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from flask_mail import Mail, Message
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
from tickets_tabledef import *
from flask_sqlalchemy import SQLAlchemy
import uuid



#Create interface with the database
engine = create_engine('sqlite:///login.db', echo=True)


#Make the application object as an instance of Flask
app = Flask(__name__ , static_url_path='/static')

#Configure the database to take login data already given
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
db = SQLAlchemy(app) 

global POST_USERNAME

#Create an instance of mail from the Mail class available in flask_mail
#pass the application object as an argument
mail = Mail(app)
def Config(app):
    '''
    Used to set the environment variables necessary
    for proper functioning of the mail feature
    '''
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'lightscamerapopcorn.nec@gmail.com'
    app.config['MAIL_PASSWORD'] = 'Popcorn@123'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
Config(app)
mail = Mail(app)





@app.route('/')
def landing():
    return render_template('landingpage2.html')

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return render_template('login2.html')
    else:
        sep = '@'
        user_name=POST_USERNAME.split(sep,1)[0]
        return render_template('home.html',user_name=user_name)
        #"Hello Boss!  <a href='/logout'>Logout</a>"

@app.route('/login', methods=['POST'])
def do_login():
    ''' 
    For login of already registered users
    '''
    global POST_USERNAME 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), 
                    User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
        return render_template('signup2.html')
    return home()
 
@app.route("/logout")
def logout():
    ''' 
    Logging out from your account
    '''
    session['logged_in'] = False
    return landing()

@app.route("/signup", methods=['GET','POST'])
def signup():
    '''
    For the Sign up of new users, adding their
    details to the database and an email confirmation 
    of sign up is performed
    '''
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']
        phno = request.form['phno']
        new_user = User(username=uname, password=passwd, phno=phno)
        db.session.add(new_user)
        db.session.commit()
        msg = Message("LightsCameraPopcorn", sender='lightscamerapopcorn.nec@gmail.com',\
                       recipients=[uname])
        msg.body = ''' Hello,
                       Your fresh popcorns are waiting for you and the smell
                       of butter is irrestible. Thank you for joining us.
                       
                       
                       Login now to book. Your password is %s''' % (passwd)
    
        mail.send(msg)        
        return render_template('login2.html')
    return render_template('signup2.html')

@app.route("/bookseats" , methods=['GET','POST'])
def bookseats():
    '''
    Booking of seats
    '''    
    if request.method == 'POST':
        city = request.form['cities']
        theatre = request.form['theatres_list']
        movie = request.form['movies_list']
        show = request.form['shows']
        return render_template('bookseats2.html', city=city,theatre=theatre,movie=movie,show=show)

@app.route("/ticketconfirm", methods=['GET','POST'])
def ticketconfirm():
    ticket_id = str(uuid.uuid4())
    email = POST_USERNAME
    if request.method == 'POST':
        city = request.form['cities']
        theatre = request.form['theatres_list']
        movie = request.form['movies_list']
        show = request.form['shows']
        new_ticket = Ticket(ticket_id=ticket_id, username=email, city_name=city, theatre_name=theatre, movie_name=movie,  show_time=show)
        db.session.add(new_ticket)
        db.session.commit()
        msg = Message("Ticket_Confirmation", sender='lightscamerapopcorn.nec@gmail.com',\
                       recipients=[email])
        msg.body = ''' Thank you for using lights camera popcorn to book your tickets!
                       
                       
                       Please show your unique ticket ID  %s at the counter and enjoy that fantastic movie with popcorns!''' % (ticket_id)
    
        mail.send(msg)
        flash('''Your ticket is booked and a confirmation is sent to you via email on your registered email address!

                Thank You for using Lights Camera Popcorn! Arigatou Gosaimasu! :) ''')
        return render_template('home.html',user_name=POST_USERNAME)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)