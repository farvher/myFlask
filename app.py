from flask import *

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///article.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from db import Article,Category

db.drop_all()
db.create_all()
db.session.commit()

@app.route('/')
def articles():
    return render_template('articles.html', articles=Article.query.all())


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



if __name__ == '__main__':
    app.run()
