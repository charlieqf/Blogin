"""
# coding:utf-8
@Author  : charles feng
@File    : index_bp
"""
import datetime
from datetime import timedelta
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from blogin.models import VisitStatistics, CommentStatistics, LikeStatistics

from blogin.decorators import permission_required

index_bp_be = Blueprint('index_bp_be', __name__, url_prefix='/backend')


@index_bp_be.route('/admin/index/')
@login_required
@permission_required
def index():
    comments, likes, visits = get_today_traffic()
    return render_template('backend/index.html', visits=visits, comments=comments, likes=likes)


@index_bp_be.route('/admin/index/', methods=['POST'])
@login_required
@permission_required
def get_recent_7days_traffics():
    days = []
    result = []
    vst_data = []
    cst_data = []
    lst_data = []
    td = datetime.date.today()
    vsts = VisitStatistics.query.filter(VisitStatistics.date > td - timedelta(days=7)).all()
    csts = CommentStatistics.query.filter(CommentStatistics.date > td - timedelta(days=7)).all()
    lsts = LikeStatistics.query.filter(LikeStatistics.date > td - timedelta(days=7)).all()
    for vst in vsts:
        days.append(str(vst.date))
        vst_data.append(vst.times)
    for cst in csts:
        cst_data.append(cst.times)
    for lst in lsts:
        lst_data.append(lst.times)

    result.append(vst_data)
    result.append(cst_data)
    result.append(lst_data)
    return jsonify({'result': result, 'days': days})


def get_today_traffic():
    date = datetime.date.today()
    vst = VisitStatistics.query.filter_by(date=date).first()
    cst = CommentStatistics.query.filter_by(date=date).first()
    lst = LikeStatistics.query.filter_by(date=date).first()
    if vst is None:
        visits = 0
    else:
        visits = vst.times
    if cst is None:
        comments = 0
    else:
        comments = cst.times
    if lst is None:
        likes = 0
    else:
        likes = lst.times
    return comments, likes, visits


