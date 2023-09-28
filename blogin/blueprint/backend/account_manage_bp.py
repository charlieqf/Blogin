"""
# coding:utf-8
@Time    : 2020/10/12
@Author  : jiangwei
@File    : user_manage_bp
@Software: PyCharm
"""
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from blogin.models import User, BlogComment, PhotoComment
from blogin.extension import db
from flask_login import login_required
from blogin.decorators import permission_required

user_m_bp = Blueprint('user_m_bp', __name__, url_prefix='/backend/interactive')


@user_m_bp.route('/index/')
@login_required
@permission_required
def index():
    page = request.args.get('page', type=int, default=1)
    pagination = User.query.order_by(User.create_time).paginate(page=page,
                                                                per_page=current_app.config['LOGIN_LOG_PER_PAGE'])
    users = pagination.items
    return render_template('backend/user-manager.html', pagination=pagination, users=users)


@user_m_bp.route('/set-admin/<int:user_id>/')
@login_required
@permission_required
def set_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.role_id = 1
    db.session.commit()
    flash('操作成功~', 'success')
    return redirect(url_for('.index'))


@user_m_bp.route('/set-user/<int:user_id>/')
@login_required
@permission_required
def set_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.email == 'charlieqf@gmail.com':
        flash('该账号是超级号，禁止操作!', 'danger')
        return redirect(url_for('.index'))
    user.role_id = 2
    db.session.commit()
    flash('操作成功~', 'success')
    return redirect(url_for('.index'))


@user_m_bp.route('/lock/<int:user_id>/')
@login_required
@permission_required
def lock(user_id):
    user = User.query.get_or_404(user_id)
    if user.email == 'charlieqf@gmail.com':
        flash('该账号是超级号，禁止操作!', 'danger')
        return redirect(url_for('.index'))
    user.status = 2
    db.session.commit()
    flash('操作成功~', 'success')
    return redirect(url_for('.index'))


@user_m_bp.route('/unlock/<int:user_id>/')
@login_required
@permission_required
def unlock(user_id):
    user = User.query.get_or_404(user_id)
    user.status = 1
    db.session.commit()
    flash('操作成功~', 'success')
    return redirect(url_for('.index'))


@user_m_bp.route('/blog-comment/')
@login_required
@permission_required
def blog_comment():
    page = request.args.get('page', default=1, type=int)
    pagination = BlogComment.query.order_by(BlogComment.timestamp).paginate(page=page,
                                                                            per_page=current_app.config[
                                                                                'LOGIN_LOG_PER_PAGE'])
    comments = pagination.items
    return render_template('backend/blog-comments.html', comments=comments, pagination=pagination)


@user_m_bp.route('/lock/blog-comment/<int:com_id>')
@login_required
@permission_required
def unlock_or_lock_blog_comment(com_id):
    blog_com = BlogComment.query.get_or_404(com_id)
    if blog_com is not None and blog_com.delete_flag == 1:
        blog_com.delete_flag = 0
    else:
        blog_com.delete_flag = 1
    db.session.commit()
    flash('操作成功!', 'success')
    return redirect(url_for('.blog_comment'))


@user_m_bp.route('/photo-comment/')
@login_required
@permission_required
def photo_comment():
    page = request.args.get('page', default=1, type=int)
    pagination = PhotoComment.query.order_by(PhotoComment.timestamp).paginate(page=page,
                                                                            per_page=current_app.config[
                                                                                'LOGIN_LOG_PER_PAGE'])
    comments = pagination.items
    return render_template('backend/photo-comments.html', comments=comments, pagination=pagination)


@user_m_bp.route('/lock/photo-comment/<int:com_id>')
@login_required
@permission_required
def unlock_or_lock_photo_comment(com_id):
    photo_com = PhotoComment.query.get_or_404(com_id)
    if photo_com is not None and photo_com.delete_flag == 1:
        photo_com.delete_flag = 0
    else:
        photo_com.delete_flag = 1
    db.session.commit()
    flash('操作成功!', 'success')
    return redirect(url_for('.photo_comment'))


@user_m_bp.route('/reset-password/<int:user_id>/')
@login_required
@permission_required
def reset_user_password(user_id):
    user = User.query.get_or_404(user_id)
    user.set_password('12345678')
    db.session.commit()
    flash('用户密码重置成功!', 'success')
    return redirect(request.referrer)
