from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from scw import db
from ..forms import SanswerForm
from scw.models import Studyboard, Sanswer
from .auth_views import login_required

bp = Blueprint('sanswer', __name__, url_prefix='/study_answer')


@bp.route('/post/<int:studyboard_id>', methods=('POST',))
@login_required
def create(studyboard_id):
    form = SanswerForm()
    studyboard = Studyboard.query.get_or_404(studyboard_id)
    if form.validate_on_submit():
        content = request.form['content']
        sanswer = Sanswer(content=content, create_date=datetime.now(), user=g.user)
        studyboard.sanswer_set.append(sanswer)
        db.session.commit()
        return redirect('{}#sanswer_{}'.format(
            url_for('studyboard.detail', studyboard_id=studyboard_id), sanswer.id))
    return render_template('studyboard/studyboard_detail.html', studyboard=studyboard, form=form)

@bp.route('/modify/<int:sanswer_id>', methods=('GET', 'POST'))
@login_required
def modify(sanswer_id):
    sanswer = Sanswer.query.get_or_404(sanswer_id)
    if g.user != sanswer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('studyboard.detail', studyboard_id=sanswer.studyboard.id))
    if request.method == "POST":
        form = SanswerForm()
        if form.validate_on_submit():
            form.populate_obj(sanswer)
            sanswer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#sanswer_{}'.format(
                url_for('studyboard.detail', studyboard_id=sanswer.studyboard.id), sanswer.id))
    else:
        form = SanswerForm(obj=sanswer)
    return render_template('sanswer/sanswer_form.html', form=form)