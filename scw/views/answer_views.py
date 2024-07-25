from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from scw import db
from ..forms import AnswerForm
from scw.models import Freeboard, Answer
from .auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/post/<int:freeboard_id>', methods=('POST',))
@login_required
def create(freeboard_id):
    form = AnswerForm()
    freeboard = Freeboard.query.get_or_404(freeboard_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        freeboard.answer_set.append(answer)
        db.session.commit()
        return redirect('{}#answer_{}'.format(
            url_for('freeboard.detail', freeboard_id=freeboard_id), answer.id))
    return render_template('freeboard/freeboard_detail.html', freeboard=freeboard, form=form)

@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('freeboard.detail', freeboard_id=answer.freeboard.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#answer_{}'.format(
                url_for('freeboard.detail', freeboard_id=answer.freeboard.id), answer.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', form=form)