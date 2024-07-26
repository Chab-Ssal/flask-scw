from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
3/0  # 강제로 오류발생
def index():
    return render_template('mainpage.html')

@bp.route('/freeboard')
def freeboard():
    return redirect(url_for('freeboard._list'))

@bp.route('/lunch')
def lunch():
    return render_template('lunch.html')

@bp.route('/potato')
def potato():
    return redirect(url_for('potato._list'))

@bp.route('/studyboard')
def studyboard():
    return redirect(url_for('studyboard._list'))