from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from scw.models import Studyboard
from scw.views.auth_views import login_required

from .. import db
from ..models import Studyboard, Sanswer, User
from ..forms import StudyboardForm, SanswerForm

bp = Blueprint('studyboard', __name__, url_prefix='/studyboard')

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    studyboard_list = Studyboard.query.order_by(Studyboard.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Sanswer.studyboard_id, Sanswer.content, User.username) \
            .join(User, Sanswer.user_id == User.id).subquery()
        studyboard_list = studyboard_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.studyboard_id == Studyboard.id) \
            .filter(Studyboard.subject.ilike(search) |  # 질문 제목
                    Studyboard.content.ilike(search) |  # 질문 내용
                    User.username.ilike(search) |  # 질문 작성자
                    sub_query.c.content.ilike(search) |  # 답변 내용
                    sub_query.c.username.ilike(search)  # 답변 작성자
                    ) \
            .distinct()
    studyboard_list = studyboard_list.paginate(page=page, per_page=15)
    return render_template('studyboard/studyboard_list.html', studyboard_list= studyboard_list, page=page, kw=kw)

@bp.route('/detail/<int:studyboard_id>/')
def detail(studyboard_id):
    form = SanswerForm()
    studyboard = Studyboard.query.get_or_404(studyboard_id)
    return render_template('studyboard/studyboard_detail.html', studyboard=studyboard, form=form) 

@bp.route('/post/', methods=('GET', 'POST'))
@login_required
def create():
    form = StudyboardForm()
    if request.method == 'POST' and form.validate_on_submit():
        studyboard = Studyboard(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(studyboard)
        db.session.commit()
        return redirect(url_for('studyboard._list'))
    return render_template('studyboard/studyboard_form.html', form=form)

@bp.route('/modify/<int:studyboard_id>', methods=('GET', 'POST'))
@login_required
def modify(studyboard_id):
    studyboard = Studyboard.query.get_or_404(studyboard_id)
    if g.user != studyboard.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('studyboard.detail', studyboard_id=studyboard_id))
    if request.method == 'POST':  # POST 요청
        form = StudyboardForm()
        if form.validate_on_submit():
            form.populate_obj(studyboard)
            studyboard.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('studyboard.detail', studyboard_id=studyboard_id))
    else:  # GET 요청
        form = StudyboardForm(obj=studyboard)
    return render_template('studyboard/studyboard_form.html', form=form)

@bp.route('/delete/<int:studyboard_id>')
@login_required
def delete(studyboard_id):
    studyboard = Studyboard.query.get_or_404(studyboard_id)
    if g.user != studyboard.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('studyboard.detail', studyboard_id=studyboard_id))
    db.session.delete(studyboard)
    db.session.commit()
    return redirect(url_for('studyboard._list'))

@bp.route('/vote/<int:studyboard_id>/')
@login_required
def vote(studyboard_id):
    _studyboard = Studyboard.query.get_or_404(studyboard_id)
    if g.user == _studyboard.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _studyboard.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('studyboard.detail', studyboard_id=studyboard_id))
