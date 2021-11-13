from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from ..models import User, Quote
from flask_login import login_required,current_user
from .forms import UpdateProfile

from .. import db,photos
from ..requests import get_quote
from .forms import UpdateProfile
from flask.views import View,MethodView


#views
@main.route('/')
def index():
    
    '''
    View root page function that returns the index page and its data.
    '''
    quote = get_quote()
    
    return render_template('index.html', quote = quote)

