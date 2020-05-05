from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile
from ..models import User,Post,Comment,Upvote,Downvote
from flask_login import login_required, current_user
from .. import db,photos



@main.route('/')

def index():
    posts = Post.query.all()
    pick_up = Post.query.filter_by(category = 'pickup_line').all() 
    product = Post.query.filter_by(category = 'product').all()
    business = Post.query.filter_by(category = 'business').all()
    return render_template('index.html', pick_up = pick_up, product = product, business = business, posts = posts)




@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username = name).first()
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


