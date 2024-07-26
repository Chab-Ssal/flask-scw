from flask import Blueprint, url_for, render_template, current_app
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def index():
    current_app.logger.info("INFO 레벨로 출력")
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