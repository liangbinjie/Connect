from flask import Blueprint, render_template, request, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from .models import Links, User
from . import UPLOAD_FOLDER, db
from .functions import check_url


edit = Blueprint('edit', __name__)

@edit.route('/edit-profile')
@login_required
def edit_profile():
    name = current_user.username
    user_lnks = current_user.links
    user_img = f'static/uploads/{str(current_user.id)}.jpg'
    return render_template('/edit/edit_profile.html', name=name, lnks=user_lnks, description=current_user.description, pfp=user_img)


@edit.route('/edit-lnk/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_profile_link(id):
    
    link = Links.query.filter_by(id=id).first()
    
    if current_user.id == link.user_id:
        if request.method == 'POST':
            link.title = request.form['title']
            link.url = request.form['url']

            db.session.commit()
            return redirect(url_for('edit.edit_profile'))

        return render_template('/edit/edit_link.html', url=link.url, title=link.title, link=link)

    else: 
        return render_template('404.html')



@edit.route('/delete-lnk/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_lnk(id):
    link_to_delete = Links.query.filter_by(id=id).first()

    db.session.delete(link_to_delete)
    db.session.commit()
    return redirect(url_for('edit.edit_profile'))



@edit.route('/add')
@login_required
def add():
    return render_template('/edit/add_link.html')


@edit.route('/add', methods=['POST'])
@login_required
def add_link():
    title = request.form.get('title')
    url = request.form.get('url')
    user_id = current_user.id

    if len(title) >= 1 and len(url) >= 1:
        new_lnk = Links(title=title.title(), url=check_url(url).lower(), user_id=user_id)

        db.session.add(new_lnk)
        db.session.commit()
    
    else:
        flash('You cannot leave blank spaces')
        return redirect(url_for('edit.add'))

    return redirect(url_for('edit.edit_profile'))


@edit.route('/profile-config')
@login_required
def profile_config():
    return render_template('/edit/profile_config.html', description=current_user.description)

import base64
@edit.route('/profile-config', methods=['GET', 'POST'])
@login_required
def profile_config_post():
    user = User.query.filter_by(id=current_user.id).first()
    if current_user.id == user.id:
        if request.method == 'POST':
            
            if 'pfp' not in request.files:
                pass
            pfp = request.files['pfp']
            if pfp.filename == '':
                pass
            
            if pfp:
                upFile = request.files['pfp'].read()
                user.pfp = base64.b64encode(upFile)

            user.description = request.form['description']
            

            db.session.commit()

            return redirect(url_for('main.profile'))

        return render_template('profile.html', description=user.description)

    else: 
        return render_template('404.html')
