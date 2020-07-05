from datetime import datetime
from app import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    sub_title = db.Column(db.String(500))
    body = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    lecture_time = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)
    category = db.relationship('Category',
                               backref=db.backref('posts', lazy=True))

    def __init__(self, title, sub_title, body, author, lecture_time, category_id):
        self.title = title
        self.sub_title = sub_title
        self.body = body
        self.author = author
        self.lecture_time = lecture_time
        self.category_id = category_id

    def __repr__(self):
        return '<Article %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category : %r>'.format(self.name)

