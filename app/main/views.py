from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from ..models import User, Quote, Blog,Comment,Subscriber
from flask_login import login_required,current_user


from .. import db,photos
from ..requests import get_quote
from .forms import BlogForm,UpdateProfile, CommentForm,UpdateBlog
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
        new_blog = Blog(title=title,user=current_user,category=category, content=content, created_by= created_by)
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


@main.route('/comment', methods=['GET', 'POST'])
@login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(name=form.name.data)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully.')
        return redirect(url_for('.index'))
    return render_template('comments.html', form=form)

@main.route('/blog/<id>', methods=['GET', 'POST'])
@login_required
def blog_details(id):
    comments = Comment.query.filter_by(blog_id=id).all()
    blogs = Blog.query.get(id)
    if blogs is None:
        abort(404)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            comment=form.comment.data,
            blog_id=id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        form.comment.data = ''
        flash('Your comment has been posted successfully!')
    return render_template('comment.html', blog=blogs, comment=comments, comment_form=form)

@main.route('/updateblog/<int:blog_id>', methods=["GET", "POST"])
def edit_blog(blog_id):
    form = UpdateBlog()
    if form.validate_on_submit():
        updates = form.updates.data
        blogs = Blog.query.filter_by(id = blog_id).updates({"updates":updates})
        db.session.commit()
        return redirect(url_for("main.profile", uname = current_user.username))
    else:
        form.updates.data = Blog.query.filter_by(id = blog_id).first()
    return render_template("edit_blog.html",updateblog_form = form)


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

# delete comment
@main.route('/comment/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    """
        View delete comment function that returns the delete comment page and its data
    """
    comment = Comment.query.filter_by(id=id).first()
    db.session.delete(comment)
    db.session.commit()
   
    
  
    flash('You have successfully deleted the comment', 'success')
    return redirect(url_for('main.profile', uname=current_user.username))

@main.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    """
         subscribe function that subscribes the user to the post
    """
    email = request.args.get('email')
    new_subscriber = Subscriber(email=email)
    db.session.add(new_subscriber)
    db.session.commit()
    flash('Email submitted successfully', 'success')
    return redirect(url_for('main.index'))