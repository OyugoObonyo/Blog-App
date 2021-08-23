from flask import render_template
from app import application
from app import forms
from app.forms import LoginForm

@application.route('/')
@application.route('/home')
def home():
    user = {'username': 'Bruno'}
    posts = [
        {
            "author": {"username": "John"},
            "body": "Looks like a beautiful day today!"
        },
        {
            "author": {"username": "Abby"},
            "body": "Who is in town today?"
        }     
    ]
    return render_template('index.html', user=user, posts=posts)

@application.route('/Login')
def login():
    form = LoginForm
    return render_template('login.html', title='Log in', form=form)