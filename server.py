#!flask/bin/python
import os  
from flask import Flask, jsonify, render_template, request, url_for, Response, make_response, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from algorithm import fair_use_determination
import flask_whooshalchemy as wa
#from whitenoise import WhiteNoise

#app = WhiteNoise(Flask(__name__), root='static/')
app = Flask(__name__, static_folder='static')
#app = Flask(__name__)

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
#app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')

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

@app.route("/add")
def add():
    # script to run through all of the files 
    for file in os.listdir('/Users/Shanelle/Downloads/pdfs'):
        if file.endswith('.pdf'):
            file_in = '/Users/Shanelle/Downloads/pdfs/' + file 
            print file_in
            file_out = '/Users/Shanelle/Desktop/Yale/SophmoreYear/Projects/IPLawFinal/ip-search' + '/textfiles/' + file.strip('pdf') + 'txt'
            print file_out
            os.system('touch '+ file_out)
            os.system('python pdf2txt.py -o ' + file_out + ' ' + file_in)
            with open(file_in, 'r') as pdf_file:
                original = pdf_file.read()
                with open(file_out, 'r') as text_file:
                    text_content = text_file.read().decode('utf-8')
                    file_name = file.strip('pdf')
                    post = Document(name=file_name, text=text_content, original = original)
                    db.session.add(post)
                    db.session.commit()
                    print 'added to database'



@app.route('/query_results', methods= ['POST'])
def query_results():
    determination = fair_use_determination(request)
    print determination
    results = Document.query.whoosh_search(request.form.get('query')).all()
    return render_template("results_list.html", results=results, determination = determination)

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
	   return render_template('form.html')

@app.route('/algorithm', methods=['GET'])
def algorithm():
    return render_template('about.html')

@app.route('/thanks', methods=['GET'])
def thanks():
    return render_template('thanks.html')

@app.route('/readme', methods=['GET'])
def readme():
    return render_template('readme.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    query = request.args.get('q')
    file_name = query + 'pdf'
    # print file_name
    # file_path = os.getcwd() + '/pdfs/' + query + 'pdf'
    # if os.path.isfile(file_path):
    #return send_static_file(file_name)
    return send_from_directory(app.static_folder, file_name)
    #return send_from_directory('pdfs', file_name)
    #return render_template("results.html", results=results)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
