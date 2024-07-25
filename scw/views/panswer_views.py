from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from scw import db
from ..forms import PanswerForm
from scw.models import Potato, Panswer
from .auth_views import login_required

bp = Blueprint('panswer', __name__, url_prefix='/potato_answer')


@bp.route('/post/<int:Potato_id>', methods=('POST',))
@login_required
def create(potato_id):
    form = PanswerForm()
    potato = Potato.query.get_or_404(potato_id)
    if form.validate_on_submit():
        content = request.form['content']
        panswer = Panswer(content=content, create_date=datetime.now(), user=g.user)
        potato.panswer_set.append(panswer)
        db.session.commit()
        return redirect('{}#panswer_{}'.format(
            url_for('Potato.detail', potato_id=potato_id), panswer.id))
    return render_template('Potato/Potato_detail.html', potato=potato, form=form)

@bp.route('/modify/<int:panswer_id>', methods=('GET', 'POST'))
@login_required
def modify(panswer_id):
    panswer = Panswer.query.get_or_404(panswer_id)
    if g.user != panswer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('Potato.detail', Potato_id=panswer.Potato.id))
    if request.method == "POST":
        form = PanswerForm()
        if form.validate_on_submit():
            form.populate_obj(panswer)
            panswer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#panswer_{}'.format(
                url_for('Potato.detail', Potato_id=panswer.Potato.id), panswer.id))
    else:
        form = PanswerForm(obj=panswer)
    return render_template('panswer/panswer_form.html', form=form)