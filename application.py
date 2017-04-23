from cs50 import SQL
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import gettempdir



from helpers import *

# configure application
app = Flask(__name__)
@app.template_filter("price")
def price(value):
    """TODO"""
    return "${:,.2f}".format(value)

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library
db = SQL("sqlite:///pset7.db")

@app.route("/")
@login_required