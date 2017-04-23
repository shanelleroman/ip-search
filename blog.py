from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wa

app = Flask(__name__)

#setting the congfig values
#appconfig['SQLALCHEMY_DATABASE_URI'] = 'mysql://prettypr_search:prettyprinted@prettyprinted.com/prettypr_whoosh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
#really important: sql track modifications: allows whoosh alcehemy to know
#when something changes in the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#creates debug object
app.config['DEBUG'] = True
#adding whoosh alechemy functionality into the thing
#place for the index to be server
#going to be stored on your server
app.config['WHOOSH_BASE'] = 'whoosh'

db = SQLAlchemy(app)
class Post(db.Model):
    __searchable__ = ['title', 'content']
    id= db.Column(db.Integer, primary_key=True)
    title = db.Column((db.String(100)))
    content = db.Column(db.String(1000))

wa.whoosh_index(app, Post)


@app.route("/")
def index():
    #give you all the posts
    post = Post.query.all()
    return render_template('index.html', posts = posts)

@app.route("/add")
def add():
    if request.method == 'POST':
        post = Post(title = request.form('title'), content = request.form['content'])
        db.session.add(post)
        db.session.commit()
        return redirect (url_for('index'))
    return render_template('add.html')

@app.route("/search")
def search():
    posts = Post.query.whoosh_search(request.args.get('query')).all()
    return render_template('index.html', posts = posts)
        


if __name__ == '__main__':
    app.run(debug= True)


