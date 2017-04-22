#!flask/bin/python
from flask import Flask, jsonify, render_template, request, url_for, Response, make_response


app = Flask(__name__)


@app.route('/')
def index():
	return render_template('form.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
	return render_template("results.html")
	


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
