
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *
import csv


import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

 
 # configure application
app = Flask(__name__)


df1 = pd.read_excel('entries.xlsx')
entries = df1.to_dict(orient='records')

df2 = pd.read_excel('innovatorsAll.xlsx')
innovatorsAll = df2.to_dict(orient='records')

df3 = pd.read_excel('teamMembers.xlsx')
teamMembers = df3.to_dict(orient='records')

if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter


# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = "mysql:///finance.db"

@app.route("/home")
def home():

    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")
'''
@app.route("/search")
def search():
    return render_template("search.html")'''
@app.route("/innovators")
def innovators():
    return render_template("innovatorList.html", innovatorsAll=innovatorsAll)

@app.route("/innovator", methods=["POST"])
def innovator():
    title = request.form['sub']
    print("The email address is '" + title + "'")
    info = [innovator for innovator in innovatorsAll if ['name'] == title]
    return render_template("intervention.html",title=title, info=info)
@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/profile")
def profile():
    return render_template("home.html")


@app.route("/team")
def team():
    return render_template("meetTheTeam.html", teamMembers=teamMembers)

@app.route("/talk")
def talk():
    return render_template("home.html")

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/intervention", methods=["POST"])
def intervention():
    title = request.form['sub']
    print("The email address is '" + title + "'")
    info = [intervention for intervention in entries if intervention['title'] == title]
    print("info", info)
    return render_template("intervention.html",title=title, info=info[0])

@app.route("/search", methods=["GET", "POST"])
def search():
    """Enable user to buy a stock."""

    # POST
    if request.method == "POST":

        # validate form submission
        if not request.form.get("intervention"):
            return render_template("results.html", results=entries)
        ''' 
        elif not request.form.get("setting"):
            return apology("missing setting")
        elif not request.form.get("emrpref"):
            return apology("missing emr pref")
        elif not request.form.get("budget"):
            return apology("missing budget")'''
        

        results = []
        print("intervention", request.form.get("intervention") )
        ''''
        for index, row in entries.iterrows():
            print("row", row)
            keywords = row['keywords']
            print("dtf", keywords)
            keywords = [x.strip() for x in keywords.split(',')]
            print("heyy", keywords)
            print(request.form.get("intervention") )
            if request.form.get("intervention") in keywords:
                results.append(row)
        '''
        
        entries_stringed = {}
        for k in entries:
            print("hehrere", k['keywords'])
            if request.form.get("intervention") in k['keywords']:
                results.append(k)
            entries_stringed[k['title']]=str(k)
        
        print("string cheese", entries_stringed)

        return render_template("results.html", results=results, entries=entries_stringed)


    # GET
    else:
        return render_template("search.html")
'''
@app.route("/index")
def index():
    """Display user's portfolio of stocks, cash balance, and grand total."""

    # query database for user's cash
    rows = entries[id] db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    if not rows:
        abort("missing user")
    cash = ["cash"]
    total = cash

    # query database for user's stocks
    stocks = db.execute("""SELECT symbol, SUM(shares) AS shares FROM transactions
        WHERE user_id = :user_id GROUP BY symbol HAVING SUM(shares) > 0""", user_id=session["user_id"])

    # query Yahoo for stocks' latest names and prices
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        total += stock["shares"] * quote["price"]

    # render portfolio
    return render_template("index.html", cash=cash, stocks=stocks, total=total)

@app.route("/buy", methods=["GET", "POST"])

def buy():
    """Enable user to buy a stock."""

    # POST
    if request.method == "POST":

        # validate form submission
        if not request.form.get("symbol"):
            return apology("missing symbol")
        elif not request.form.get("shares"):
            return apology("missing shares")
        elif not request.form.get("shares").isdigit():
            return apology("invalid shares")
        shares = int(request.form.get("shares"))

        # get stock quote
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("invalid symbol")

        # cost to buy
        cost = shares * quote["price"]

        # get user's cash balance
        rows = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        if not rows:
            abort("missing user")
        cash = rows[0]["cash"]

        # ensure user can afford
        if cash < cost:
            return apology("can't afford")

        # record purchase
        db.execute("""INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES(:user_id, :symbol, :shares, :price)""",
            user_id=session["user_id"], symbol=quote["symbol"], shares=shares, price=quote["price"])

        # deduct cash
        db.execute("UPDATE users SET cash = cash - :cost WHERE id = :id", cost=cost, id=session["user_id"])

        # display portfolio
        flash("Bought!")
        return redirect(url_for("index"))

    # GET
    else:
        return render_template("buy.html")

@app.route("/history")

def history():
    """Display user's history of transactions."""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])
    return render_template("history.html", transactions=transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])

def quote():
    """Get a stock quote."""

    # POST
    if request.method == "POST":

        # validate form submission
        if not request.form.get("symbol"):
            return apology("missing symbol")

        # get stock quote
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("invalid symbol")

        # display quote
        return render_template("quoted.html", quote=quote)

    # GET
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user for an account."""

    # POST
    if request.method == "POST":

        # validate form submission
        if not request.form.get("username"):
            return apology("missing username")
        elif not request.form.get("password"):
            return apology("missing password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        # hash password
        hash = pwd_context.encrypt(request.form.get("password"))

        # add user to database
        id = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
            username=request.form.get("username"), hash=hash)
        if not id:
            return apology("username taken")

        # log user in
        session["user_id"] = id

        # let user know they're registered
        flash("Registered!")
        return redirect(url_for("index"))

    # GET
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])

def sell():
    """Enable user to sell a stock."""

    # POST
    if request.method == "POST":

        # validate form submission
        if not request.form.get("symbol"):
            return apology("missing symbol")
        symbol = request.form.get("symbol").upper()
        if not request.form.get("shares"):
            return apology("missing shares")
        elif not request.form.get("shares").isdigit():
            return apology("invalid shares")
        shares = int(request.form.get("shares"))

        # check how many shares user owes
        rows = db.execute("""SELECT SUM(shares) AS shares FROM transactions
            WHERE user_id = :user_id AND symbol = :symbol GROUP BY symbol""",
            user_id=session["user_id"], symbol=symbol)
        if len(rows) != 1:
            return apology("symbol not owned")
        if shares > rows[0]["shares"]:
            return apology("too many shares")

        # get stock quote
        quote = lookup(request.form.get("symbol"))

        # record sale
        db.execute("""INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES(:user_id, :symbol, :shares, :price)""",
            user_id=session["user_id"], symbol=quote["symbol"], shares=-shares, price=quote["price"])

        # deposit cash
        db.execute("UPDATE users SET cash = cash + :value WHERE id = :id",
            value=shares*quote["price"], id=session["user_id"])

        # display portfolio
        flash("Sold!")
        return redirect(url_for("index"))

    # GET
    else:
        return render_template("sell.html")'''
