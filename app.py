from datetime import datetime

from flask import *
from extractor import Extractor
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///article.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    sub_title = db.Column(db.String(500))
    body = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    lecture_time = db.Column(db.Integer)
    img = db.Column(db.String(100))

    def __init__(self, title, sub_title, body, author, lecture_time, img):
        self.title = title
        self.sub_title = sub_title
        self.body = body
        self.author = author
        self.lecture_time = lecture_time
        self.img = img

    def __repr__(self):
        return '<Article %r>' % self.title


db.drop_all()
db.create_all()


@app.route('/')
def articles():
    return render_template('articles.html', articles=Article.query.all())


@app.route('/extractor')
def extractor():
    ex = Extractor("https://www.pulzo.com/")
    ex.search_href_recursive()
    hrefs = ex.my_href
    hrefs = dict.fromkeys(hrefs)

    for h in hrefs:
        try:
            article = ex.extract_article(h)
            print(article)
            art = Article(title=article['title'],
                          sub_title=article['sub_title'],
                          body=article['body'],
                          author=article['author'],
                          lecture_time=article['lecture_time'],
                          img=article['img'])
            db.session.add(art)
            db.session.commit()
        except Exception:
            print(h + "failed!!")

    return "ok"


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['title'] or not request.form['body'] or not request.form['author']:
            flash('Please enter all the fields', 'error')
        else:
            article = Article(title=request.form['title'],
                              sub_title=request.form['subtitle'],
                              body=request.form['body'],
                              author=request.form['author'],
                              lecture_time=5,
                              category_id=1)

            db.session.add(article)
            db.session.commit()

            flash('Record was successfully added')
            return redirect(url_for('articles'))
    return render_template('new.html')
