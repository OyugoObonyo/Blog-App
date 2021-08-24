from flask import render_template, flash, redirect, url_for
from app import application
from app.forms import LoginForm


@application.route('/')
@application.route('/index')
def index():
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

@application.route('/login', methods=["GET", "POST"])
def login():
    log_form = LoginForm()
    if log_form.validate_on_submit():
        flash("Login requested for user {}, remember_me={}".format(
            log_form.username.data, log_form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Log in', form=log_form)