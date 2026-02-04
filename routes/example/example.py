from flask import render_template, request, Blueprint
from database import db

home_page = Blueprint('example', __name__, url_prefix='/example')

@home_page.route('/')
def home():
    user = db.get_user_by_token(request.cookies.get('token'))
    return render_template('example/example.jinja', user=user)