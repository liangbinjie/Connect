from flask import Blueprint, render_template, request, url_for
from flask_login import login_required, current_user
from .models import Links, User
from . import UPLOAD_FOLDER, db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/my-profile')
@login_required
def profile():
    user = User.query.filter_by(id=current_user.id).first()

    name = current_user.username
    user_lnks = current_user.links
    description = current_user.description
    user_img = current_user.pfp

    return render_template('profile.html', name=name, lnks=user_lnks, description=description, pfp='data:image/png;base64,' + str(user_img, 'UTF-8'))

        
@main.route('/<username>')
def profiles(username):

    user = User.query.filter_by(username=username.lower()).first()
    if user:
        user_lnks = user.links
        name = user.username
        description = user.description
        user_img = user.pfp
        

        return render_template('profiles.html', lnks=user_lnks, name=name, description=description, pfp='data:image/png;base64,' + str(user_img, 'UTF-8'))
        
    else:
        return render_template('404.html', username=username)
