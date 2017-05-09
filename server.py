#!flask/bin/python
import os  
from flask import Flask, jsonify, render_template, request, url_for, Response, make_response, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wa

app = Flask(__name__, static_folder='static')

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
    userFacingName = db.Column(db.String(255))
    text = db.Column((db.Text()))
    original = db.Column((db.BLOB()))



wa.whoosh_index(app, Document)

# @app.route("/add")
# def add():
#     db.session.
#     # script to run through all of the files 
#     for file in os.listdir('./pdfs'):
#         if file.endswith('.pdf'):
#             file_in = os.getcwd() +  '/pdfs/' + file 
#             file_out = os.getcwd() + '/textfiles/' + file.strip('pdf') + 'txt'
#             with open(file_in, 'r') as pdf_file:
#                 original = pdf_file.read()
#                 with open(file_out, 'r') as text_file:
#                     text_content = text_file.read().decode('utf-8')
#                     file_name = file.strip('pdf')
#                     post = Document(name=file_name, text=text_content, original = original)
#                     db.session.add(post)
#                     db.session.commit()
#     pass


@app.route('/query_results', methods= ['GET', 'POST'])
def query_results():
    results = Document.query.whoosh_search(request.form.get('query')).all()
    return render_template("results_list.html", results=results)

@app.route('/')
def index():
	return render_template('form.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    query = request.args.get('q')
    file_name = query + 'pdf'
    # print file_name
    # file_path = os.getcwd() + '/pdfs/' + query + 'pdf'
    # if os.path.isfile(file_path):
    return send_from_directory(app.static_folder, file_name)
    #return send_from_directory('pdfs', file_name)
    return render_template("results.html", results=results)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
