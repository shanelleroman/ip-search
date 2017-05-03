#!flask/bin/python
from flask import Flask, jsonify, render_template, request, url_for, Response, make_response
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wa

app = Flask(__name__)

#setting the congfig values
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ip-search.db'

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
class Document(db.Model):
    #defines which columns can be searched
    __searchable__ = ['name', 'text']#three columns, one primary key
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column((db.String(30)))
    #text = db.Column(db.String(100))
    text = db.Column((db.Text()))


wa.whoosh_index(app, Document)

@app.route("/add")
def add():
    content = ''
    title = 'sample.txt'
    with open(title, 'r') as content_file:
        content = content_file.read()
        post = Document(name = title, text= content)
        db.session.add(post)
        db.session.commit()
    pass

@app.route('/')
def index():
	return render_template('form.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    results = Document.query.whoosh_search(request.form.get('query')).all()
    return render_template("results.html", results=results)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
