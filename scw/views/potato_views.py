from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from scw.models import Potato
from scw.views.auth_views import login_required

from .. import db
from ..models import Potato, Panswer, User
from ..forms import PotatoForm, PanswerForm

bp = Blueprint('potato', __name__, url_prefix='/potato')

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    potato_list = Potato.query.order_by(Potato.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Panswer.potato_id, Panswer.content, User.username) \
            .join(User, Panswer.user_id == User.id).subquery()
        potato_list = potato_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.potato_id == Potato.id) \
            .filter(Potato.subject.ilike(search) |  # 질문 제목
                    Potato.content.ilike(search) |  # 질문 내용
                    User.username.ilike(search) |  # 질문 작성자
                    sub_query.c.content.ilike(search) |  # 답변 내용
                    sub_query.c.username.ilike(search)  # 답변 작성자
                    ) \
            .distinct()
    potato_list = potato_list.paginate(page=page, per_page=15)
    return render_template('potato/potato_list.html', potato_list= potato_list, page=page, kw=kw)

@bp.route('/detail/<int:potato_id>/')
def detail(potato_id):
    form = PanswerForm()
    potato = Potato.query.get_or_404(potato_id)
    return render_template('potato/potato_detail.html', potato=potato, form=form) 

@bp.route('/post/', methods=('GET', 'POST'))
@login_required
def create():
    form = PotatoForm()
    if request.method == 'POST' and form.validate_on_submit():
        potato = Potato(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(potato)
        db.session.commit() 
        return redirect(url_for('potato._list'))
    return render_template('potato/potato_form.html', form=form)

@bp.route('/modify/<int:potato_id>', methods=('GET', 'POST'))
@login_required
def modify(potato_id):
    potato = Potato.query.get_or_404(potato_id)
    if g.user != potato.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('potato.detail', potato_id=potato_id))
    if request.method == 'POST':  # POST 요청
        form = PotatoForm()
        if form.validate_on_submit():
            form.populate_obj(potato)
            potato.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('potato.detail', potato_id=potato_id))
    else:  # GET 요청
        form = PotatoForm(obj=potato)
    return render_template('potato/potato_form.html', form=form)

@bp.route('/delete/<int:potato_id>')
@login_required
def delete(potato_id):
    potato = Potato.query.get_or_404(potato_id)
    if g.user != potato.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('potato.detail', potato_id=potato_id))
    db.session.delete(potato)
    db.session.commit()
    return redirect(url_for('potato._list'))

@bp.route('/vote/<int:potato_id>/')
@login_required
def vote(potato_id):
    _potato = Potato.query.get_or_404(potato_id)
    if g.user == _potato.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _potato.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('potato.detail', potato_id=potato_id))