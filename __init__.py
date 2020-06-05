from flask import Flask
from flask import render_template, request, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length

from Database import makeUser, findUser
from Messages import find, new, findMessages, newMessage

app = Flask(__name__)

app.config['SECRET_KEY'] = 'wg&}#*%#^&qqvq](rwq)cdr)p!sd{u%(yb}uprrhezhjmw(v]g'


class Signup(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    name = StringField('Name', validators=[DataRequired(), Length(max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])

class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/conversation', methods=['POST', 'GET'])
def conversation():
    if not session.get('logged_in'):
        return redirect('/login')
    elif not session.get('chatName'):
        return redirect('/choose')
    email = session.get('email')
    name = findUser(email, "name")
    chatName = session.get('chatName')
    if request.method == 'POST':
        if request.form['content']!='':
            newMessage(chatName, request.form['from'], request.form['content'])
        return redirect(f"/conversation")
    posts=findMessages(chatName)
    return render_template(f'conversation.html', posts=posts, name=name, email=email, chatName=chatName)


@app.route('/choose', methods=['POST',"GET"])
def choose():
    if not session.get('logged_in'):
        return redirect('/login')
    email = session.get('email')
    name = findUser(email, "name")

    if request.method == 'POST':
        if request.form['na'] != '' and request.form['pass'] != "":
            if request.form["pass"] == find(request.form["na"])[1]:
                session['chatName'] = request.form['na']
                return redirect("/conversation")
            else:
                flash("incorrect name or pin")

        elif request.form['new_na'] != '' and len(request.form["new_pass"]) > 3:
            if new(request.form["new_na"], request.form["new_pass"]) != "failed":
                return f"<h2>Created new!</h2> <a href=choose>continue</a>"
            else:
                flash("Chat Name is already in use!")
        else:
            flash('Pin too short!')

    return render_template("choose.html", name=name, email=email)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = Signup()
    if form.validate_on_submit():

        if makeUser(form.email.data, form.name.data, form.password.data) == 'failed':
            flash('email already exists, try a different email.')
            return render_template("signup.html", form=form)

        return f'''<h1>hello {findUser(form.email.data, "name")}</h1><a href='/login'>Log in here</a>'''

    return render_template('signup.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = Login()
    if form.validate_on_submit():
        if findUser(form.email.data) == 'failed':
            flash('incorrect email or password!')
            return render_template('login.html', form=form)
        if form.password.data != findUser(form.email.data)[2]:
            flash('incorrect email or password')
            return render_template('login.html', form=form)
        session['logged_in'] = True
        session['chatName'] = False
        session['email'] = findUser(form.email.data)[0]
        return redirect('/choose')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['email'] = None
    session['chatName'] = None
    return f"<a href='{url_for('home')}'>return home</a><script>alert('logout successful!')</script>"

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='192.168.1.26')