from flask import render_template, flash, redirect, url_for, request
from app import application, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


@application.route('/')
@application.route('/index')
@login_required
def index():
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
    return render_template('index.html', posts=posts)


@application.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Handle case where already logged-in user navigates to /login URL
        return redirect(url_for('index'))
    log_form = LoginForm()
    if log_form.validate_on_submit():
        user = User.query.filter_by(username=log_form.username.data).first()
        if user is None or not user.check_password(log_form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=log_form.remember_me.data)
        # Obtain value of next query string after log in
        next_page = request.args.get('next')
        # Redirect user to homepage if it doesn't have next arg or if next arg is set to full URL that includes domain name
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Log in', form=log_form)


@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@application.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    reg_form = RegistrationForm
    if reg_form.validate_on_submit():
        user = User(username=reg_form.username.data, email=reg_form.email.data)
        user.set_password(reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Sign up was succesful!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=reg_form)