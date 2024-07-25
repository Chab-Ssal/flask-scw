from scw import db

freeboard_voter = db.Table(
    'freeboard_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('freeboard_id', db.Integer, db.ForeignKey('freeboard.id', ondelete='CASCADE'), primary_key=True))

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True))

class Freeboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('freeboard_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=freeboard_voter, backref=db.backref('freeboard_voter_set'))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    freeboard_id = db.Column(db.Integer, db.ForeignKey('freeboard.id', ondelete='CASCADE'))
    freeboard = db.relationship('Freeboard', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))

class Potato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('potato_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)


class Panswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    potato_id = db.Column(db.Integer, db.ForeignKey('potato.id', ondelete='CASCADE'))
    potato = db.relationship('Potato', backref=db.backref('panswer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('panswer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)

studyboard_voter = db.Table(
    'studyboard_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('studyboard_id', db.Integer, db.ForeignKey('studyboard.id', ondelete='CASCADE'), primary_key=True))

sanswer_voter = db.Table(
    'sanswer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('sanswer_id', db.Integer, db.ForeignKey('sanswer.id', ondelete='CASCADE'), primary_key=True))

class Studyboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('studyboard_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=studyboard_voter, backref=db.backref('studyboard_voter_set'))

class Sanswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studyboard_id = db.Column(db.Integer, db.ForeignKey('studyboard.id', ondelete='CASCADE'))
    studyboard = db.relationship('Studyboard', backref=db.backref('sanswer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('sanswer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=sanswer_voter, backref=db.backref('sanswer_voter_set'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
