from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from ..models import User, Quote, Blog
from flask_login import login_required,current_user


from .. import db,photos
from ..requests import get_quote
from .forms import BlogForm,UpdateProfile
from flask.views import View,MethodView



#views
@main.route('/')
def index():
    '''
    View root function that returns index template
    '''

    quote = get_quote()
    blog_form = BlogForm()
    all_blogs = Blog.query.order_by(Blog.date_posted).all()
    return render_template('index.html',quote =quote,blogs = all_blogs)

@main.route('/quotes')
def quotes():

    '''
    '''
    quote = get_quote()
    title = 'Blogger | Quotes'
    
    return render_template('quotes.html', title = title,quote = quote)

@main.route('/blog', methods=['GET', 'POST'])
@login_required
def new_blog():
    blog_form = BlogForm()
    if blog_form.validate_on_submit():
        title = blog_form.blog_title.data
        category = blog_form.category.data
        content = blog_form.content.data
        created_by = blog_form.created_by.data
        new_blog = Blog(title=title,category=category, content=content, created_by= created_by)
        new_blog.save_blog()
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('main.index'))

    else:
        all_blogs = Blog.query.order_by(Blog.date_posted).all()

    return render_template('blog.html', blogs=all_blogs,blog_form = blog_form)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)
    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)
    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile', uname=user.username))
    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))

@main.route('/blog/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_blog(id):
    """
        View delete post function that returns the delete post page and its data
    """
    blog = Blog.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    flash('You have successfully deleted the post', 'success')
    return redirect(url_for('main.index'))