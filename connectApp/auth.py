from linkapp.sendmail import send
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
import flask
import flask_login
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('/auth/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username.lower()).first()

    if not user:
        flash('User doesn\'t exists')
        return redirect(url_for('auth.login'))

    elif not check_password_hash(user.password, password):
        flash('Incorrect password, try again.')
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.index'))


# [FUTURE UPADATE] Deny access to logged users 
@auth.route('/signup')
def signup():
    return render_template('/auth/signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email.lower()).first()
    usern = User.query.filter_by(username=username.lower()).first()

    if len(password) == 0:
        flash('Add a password')
        return redirect(url_for('auth.signup'))

    elif len(username) == 0:
        flash('Add a username')
        return redirect(url_for('auth.signup'))

    elif len(email) == 0:
        flash('Add a email')
        return redirect(url_for('auth.signup'))

    elif user:
        flash('Email already exists.')
        return redirect(url_for('auth.signup'))
    
    elif usern:
        flash('User already exists.')
        return redirect(url_for('auth.signup'))
    
    elif len(password) < 8:
        flash('Password too short')
        return redirect(url_for('auth.signup'))
    

    new_user = User(email=email.lower(), username=username.lower(), password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()


    flask_login.login_user(new_user)
    return redirect(url_for('edit.profile_config'))



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))




@auth.route('/change-password')
@login_required
def change_pass():
    # first get the current password
    # 
    pass