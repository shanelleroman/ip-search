#BUilding the database using SQL academy
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_whooshalchemy as wa

app = Flask(__name__)

#setting the congfig values
appconfig['SQLALCHEMY_DATABASE_URI'] = 'mysql://prettypr_search:prettyprinted@prettyprinted.com/prettypr_whoosh'
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

#creates a table 
class Course(db.Model):
	__searchable__ = [' name', 'description']
	#three columns, one primary key
	id= db.Column(db.Integer, primary_key=TRUE)
	name = db.Column(db.Column(db.String(30)))
	description = db.Column(db.String(100))

wa.whoosh_index(app, Course) 
