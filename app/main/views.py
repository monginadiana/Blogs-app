from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from ..models import User, Quote
from flask_login import login_required,current_user
from .. import db
from ..requests import get_quote


#views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data.
    '''
    return render_template('index.html')

@main.route('/quotes')
def quotes():

    '''
    '''
    quote = get_quote()
    title = 'LetsBlog | Quotes'
    
    return render_template('quotes.html', title = title,quote = quote)