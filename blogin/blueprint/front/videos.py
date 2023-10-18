from flask import Blueprint, render_template, send_from_directory, flash, redirect, request, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func
from blogin import basedir, db
from blogin.models import Video, LikeVideo, Notification, Tag, VisitStatistics, CommentStatistics, LikeStatistics
from blogin.models import VideoComment
from blogin.decorators import statistic_traffic

videos_bp = Blueprint('videos_bp', __name__, url_prefix='/videos')


@videos_bp.route('/all/', methods=['GET', 'POST'])
@statistic_traffic(db, VisitStatistics)
def index():
    videos = Video.query.filter_by(level=0).order_by(func.random()).limit(9)
    return render_template('main/videos.html', videos=videos)


@videos_bp.route('/video/<video_id>', methods=['GET', 'POST'])
def video(video_id):
    replies = []
    vid = Video.query.get_or_404(video_id)
    if vid.level == 1:
        flash('未公开的照片，禁止访问!', 'success')
        return redirect(url_for('.index'))
    nex = Video.query.filter(Video.id > video_id).order_by(Video.id.asc()).first()
    pre = Video.query.filter(Video.id < video_id).order_by(Video.id.desc()).first()
    comments = VideoComment.query.filter_by(video_id=video_id, parent_id=None).\
        order_by(VideoComment.timestamp.desc()).all()
    for comment in comments:
        reply = VideoComment.query.filter_by(parent_id=comment.id, delete_flag=0).\
                order_by(VideoComment.timestamp.desc()).all()
        replies.append(reply)
    if nex is None:
        next_link = None
    else:
        next_link = '/videos/video/' + str(nex.id)
    if pre is None:
        pre_link = None
    else:
        pre_link = '/videos/video/' + str(pre.id)
    return render_template('main/video.html', blog=vid, nextLink=next_link, preLink=pre_link,
                           comments=comments, replies=replies)


@videos_bp.route('/<path>/<filename>')
def get_blog_sample_vid(path, filename):
    path = basedir + '/uploads/videos/' + path + '/'
    return send_from_directory(path, filename)


@videos_bp.route('/like/<video_id>/')
@login_required
@statistic_traffic(db, LikeStatistics)
def like_video(video_id):
    vid = Video.query.get_or_404(video_id)
    lp = LikeVideo(user=current_user, video=vid)
    db.session.add(lp)
    db.session.commit()
    flash('点赞成功，多谢啦~', 'success')
    return redirect(request.referrer)


@videos_bp.route('/video/comment/', methods=['GET', 'POST'])
@login_required
@statistic_traffic(db, CommentStatistics)
def new_comment():
    comment = request.form.get('comment')
    blog_id = request.form.get('videoID')
    reply_id = request.form.get('replyID')
    parent_id = request.form.get('parentID')
    author = current_user._get_current_object()
    vid = Video.query.get_or_404(blog_id)
    notify = comment
    comment = VideoComment(body=comment, author=author, video=vid)
    if reply_id:
        comment.replied = VideoComment.query.get_or_404(reply_id)
        new_notify = Notification(type=1, target_id=blog_id, send_user=author.username,
                                  receive_id=comment.replied.author_id, msg=notify, target_name=vid.title)
        db.session.add(new_notify)
    if parent_id:
        comment.parent_id = parent_id
    db.session.add(comment)
    db.session.commit()
    return redirect(request.referrer)


@videos_bp.route('/comment/delete/', methods=['GET', 'POST'])
@login_required
def delete_comment():
    comm_id = request.form.get('comm_id')
    comment = VideoComment.query.get_or_404(comm_id)
    comment.delete_flag = 1
    db.session.commit()
    flash('评论删除成功', 'success')
    return ''


@videos_bp.route('/tag/<int:tag_id>/')
def tag(tag_id):
    tags = Tag.query.get_or_404(tag_id)
    videos = Video.query.with_parent(tags).filter_by(level=0).order_by(Video.create_time.desc())
    return render_template('main/videos-tag.html', videos=videos, tags=tags)
