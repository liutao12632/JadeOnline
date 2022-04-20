from flask import render_template, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from ..decorators import admin_required
from werkzeug.utils import redirect

from . import auth
from .. import db
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, EditProfileForm, EditProfileAdminForm
from ..models import User, Role


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('无效的用户名或密码')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已登出')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    address=form.address.data,
                    about_me=form.about_me.data)
        db.session.add(user)
        db.session.commit()
        flash("注册成功")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.new_password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('密码已修改!')
        else:
            flash('错误的密码.')
    return render_template("auth/change_password.html", form=form)


@auth.route('/editProfile', methods=['GET', 'POST'])
@login_required
def editProfile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.address = form.address.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('您的用户资料已修改')
        return redirect(url_for('main.user', username=current_user.username))
    form.username.data = current_user.username
    form.address.data = current_user.address
    form.about_me.data = current_user.about_me
    return render_template('auth/edit_profile.html', form=form)


@auth.route('/editProfile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editProfileAdmin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.role = Role.query.get(form.role.data)
        user.address = form.address.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('该用户资料已修改')
        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role_id
    form.address.data = user.address
    form.about_me.data = user.about_me
    return render_template('auth/edit_profile.html', form=form, user=user)
