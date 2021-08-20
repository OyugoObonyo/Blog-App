from app import application

@application.route('/')
@application.route('/home')
def home():
    return "Hello world!"