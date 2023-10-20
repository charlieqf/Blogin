import os
from datetime import datetime
import subprocess

from PIL import Image
from flask import Blueprint, render_template, flash, redirect, url_for, current_app, request
from flask_login import login_required, current_user
from blogin.setting import basedir
from blogin.blueprint.backend.forms import AddVideoForm, EditVideoInfoForm
from blogin.models import Video, Tag
from blogin.utils import create_path, update_contribution
from blogin.extension import db
from blogin.decorators import permission_required
from blogin.storage import AwsStorage

be_video_bp = Blueprint('be_video_bp', __name__, url_prefix='/backend/video')

def generate_thumbnail(video_file_path):    
    # Generate thumbnail
    thumbnail_path = video_file_path.replace(".mp4", "_thumbnail.jpg")
    subprocess.call(["ffmpeg", "-i", video_file_path, "-ss", "00:00:02", "-vframes", "1", thumbnail_path])
    
    return thumbnail_path.replace(basedir + "/uploads", "")

@be_video_bp.route('/add/', methods=['GET', 'POST'])
@login_required
@permission_required
def add_video():
    form = AddVideoForm()
    if form.validate_on_submit():
        tags = form.tags.data
        title = form.video_title.data
        video_file = form.video_file.data.filename
        video_file = str(current_user.id) + video_file
        desc = form.video_desc.data

        # 视频保存在当前日期的文件夹中
        folder = str(datetime.now()).split(' ')[0]
        create_path(basedir + '/uploads/videos/' + folder)
        full_file_path = basedir + '/uploads/videos/' + folder + '/' + video_file
        form.video_file.data.save(full_file_path)

        thumbnail_path = generate_thumbnail(full_file_path)
        print("video thumbnail created at:", thumbnail_path)
        
        # upload video file to AWS S3 bucket 'charlieqf-blog'
        s3_bucket_name = 'charlieqf-blog'
        s3_folder_path = 'blog_videos_serve/' + datetime.now().strftime('%Y-%m-%d')
        s3_file_path = f"{s3_folder_path}/{video_file}"

        aws_storage = AwsStorage()
        upload_successful = aws_storage.upload_to_s3(full_file_path, s3_bucket_name, s3_file_path)

        if not upload_successful:
            flash('Failed to upload video to S3.', 'error')
            return render_template('backend/add-video.html', form=form)
        else:
            video_path = "/" + s3_file_path
            video = Video(title=title, description=desc, save_path=video_path, thumbnail_path=thumbnail_path)
            db.session.add(video)
            
            update_contribution()
            db.session.commit()
            flash('Successfully published video!', 'success')
        return redirect(url_for('videos_bp.index'))
    
    return render_template('backend/add-video.html', form=form)


@be_video_bp.route('/edit/')
@login_required
@permission_required
def video_edit():
    page = request.args.get('page', 1, type=int)
    pagination = Video.query.order_by(Video.create_time).paginate(page=page, per_page=current_app.config['BLOGIN_PHOTO_PER_PAGE'])
    videos = pagination.items
    return render_template('backend/editVideo.html', pagination=pagination, videos=videos)


@be_video_bp.route('/private/<int:video_id>/')
@login_required
@permission_required
def private(video_id):
    video = Video.query.get_or_404(video_id)
    video.level = 1
    db.session.commit()
    flash('设为私密视频成功!', 'success')
    return redirect(url_for('.video_edit'))


@be_video_bp.route('/non-private/<int:video_id>/')
@login_required
@permission_required
def non_private(video_id):
    video = Video.query.get_or_404(video_id)
    video.level = 0
    db.session.commit()
    flash('设为公开视频成功!', 'success')
    return redirect(url_for('.video_edit'))


@be_video_bp.route('/info-edit/<int:video_id>/', methods=['GET', 'POST'])
@login_required
@permission_required
def info_edit(video_id):
    form = EditVideoInfoForm()
    video = Video.query.get_or_404(video_id)
    if form.validate_on_submit():
        video.title = form.video_title.data
        video.description = form.video_desc.data
        update_contribution()
        db.session.commit()
        return redirect(url_for('.video_edit'))
    form.video_title.data = video.title
    form.video_desc.data = video.description
    return render_template('backend/editVideoInfo.html', form=form)
