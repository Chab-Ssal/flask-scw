from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def page_not_found(e):
    return render_template('404.html'), 404
def server_error(e):
    return render_template('500.html'), 500

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')

    #ORM
    db.init_app(app)
    migrate.init_app(app, db)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from . import models

    # 블루프린트
    from .views import main_views, freeboard_views, answer_views, auth_views, potato_views, panswer_views, studyboard_views, sanswer_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(freeboard_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(potato_views.bp)
    app.register_blueprint(panswer_views.bp)
    app.register_blueprint(studyboard_views.bp)
    app.register_blueprint(sanswer_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # 오류페이지
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)

    return app