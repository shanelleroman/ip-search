#!flask/bin/python
from flask import Flask, jsonify, render_template, request, url_for, Response, make_response


app = Flask(__name__)


@app.route('/')
def index():
	return "hello world! my name is SD"
	
# takes client query, scrapes facebook group and returns json response
@app.route('/query')
def query():
	return "hello"

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
