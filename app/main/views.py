from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile,PostForm,CommentForm
from ..models import User,Post,Comment,Upvote,Downvote
from flask_login import login_required, current_user
from .. import db,photos



@main.route('/')
def index():
    all_posts = Post.query.all()
    pickup_posts = Post.query.filter_by(category = 'pickup_line').all() 
    product_posts = Post.query.filter_by(category = 'product').all()
    business_posts= Post.query.filter_by(category = 'business').all()
    return render_template('index.html',all_posts = all_posts,pickup_posts = pickup_posts,product_posts = product_posts, business_posts = business_posts )


@main.route('/pickup_lines')
def pick_up():
    posts = Post.query.filter_by(category = 'pickup_line').all() 
    return render_template('display_posts.html', posts = posts)


@main.route('/products')
def product():
    posts = Post.query.filter_by(category = 'product').all()
    return render_template('display_posts.html',posts = posts)


@main.route('/business')
def business():
    posts = Post.query.filter_by(category = 'business').all()
    return render_template('display_posts.html', posts = posts)






@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = current_user._get_current_object().id
    posts = Post.query.filter_by(user_id = user_id).all()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,posts=posts)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/new_post', methods = ['POST','GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post_title = form.title.data
        post_content = form.post.data
        category = form.category.data
        user_id = current_user._get_current_object().id
        new_post_object = Post(post_content=post_content,user_id=user_id,category=category,post_title=post_title)
        new_post_object.save()
        return redirect(url_for('main.index'))
        
    return render_template('create_post.html', form = form)






@main.route('/like/<int:id>',methods = ['POST','GET'])
@login_required
def like(id):
    post = Post.query.get(id)
    new_upvote = Upvote(post=post, upvote=1)
    new_upvote.save()
    return redirect(url_for('main.index',id=id))
    



@main.route('/dislike/<int:id>',methods = ['POST','GET'])
@login_required
def dislike(id):
    post = Post.query.get(id)
    new_downvote = Downvote(post=post, upvote=1)
    new_downvote.save()
    return redirect(url_for('main.index',id = id))
   


@main.route('/comment/<int:post_id>', methods = ['POST','GET'])
@login_required
def comment(post_id):
    form = CommentForm()
    post = Post.query.get(post_id)
    all_comments = Comment.query.filter_by(post_id = post_id).all()
    
    if form.validate_on_submit():
        comment = form.comment.data 
        post_id = post_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,post_id = post_id)
        new_comment.save()
        return redirect(url_for('.comment', post_id = post_id))
    return render_template('comment.html', form =form, post = post,all_comments=all_comments)


