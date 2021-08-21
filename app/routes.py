from flask import render_template
from app import application


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