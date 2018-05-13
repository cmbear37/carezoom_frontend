
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *



# configure application
app = Flask(__name__)

#VERSION WITHOUT SQL
global entries 
entries = {}
entries['BMC Hepatitis C'] = {'Title':'BMC Hepatitis C','Keywords':['hepatitis', 'hepatitis c', 'patient', 'pharmacist', 'care', 'population', 'medical', 'medical center', 'boston', 'disease', 'primary care', 'treatment'], 'Organization':"The intervention was implemented by the Boston Medical Center Primary Care Hepatitis C Treatment Program. Boston Medical Center (BMC) is a large safety net hospital, with 90% of the patient population enrolled in MassHealth or Medicare. 10% of the patient population has hepatitis C, much higher than the 2% hepatitis C prevalence in the United States’ general population. While some hepatitis C patients at BMC received care for hepatitis C in specialty clinics (gastrointestinal or infectious disease), a lot of patients did not receive care necessary care to treat their disease. Additionally, 340B drug pricing monetarily incentivizes medical centers to treat hepatitis C in their patient population. The Boston Medical Center Primary Care Hepatitis C Treatment Program was established in 2015 in an effort to address the specific needs of hepatitis C patients so that they can receive treatment, decreasing disease burden in the population and secondarily, financially benefit the hospital. The program consists of 13 primary care physicians (4 of whom see the majority of the patients) who have been trained in treating hepatitis C, a social worker (follows patients longitudinally, tries to help address patients’ psychosocial issues), a clinical pharmacist (provides medication teaching to patients), and a pharmacist technician (works to obtain prior authorization for hepatitis C medication). ",
"Overview":"Implemented a financial incentive program to improve appointment attendance at a safety-net hospital-based primary care hepatitis C treatment program.", 
"Implementation": "The Boston Medical Center Primary Care Hepatitis C Treatment Program’s no show rate (# missed appointments/total # appointments scheduled) was 40% during its first few years, much higher than the 25% no show rate hospital-wide. The program director decided an intervention was necessary to get patients to attend the appointments necessary to treat their disease. The team considered QI projects around patient navigation and case management, but they felt the social worker was providing these services well. The social worker mentioned that patients had reported not coming to clinic for financial reasons (unable to miss work, issues with transportation, no childcare available). They decided to try a monetary incentive program. While this has not been implemented for hepatitis C treatment, it has been shown to be effective in care for HIV, substance use disorder, and smoking cessation. They received a grant from the Boston University Center for Implementation and Improvement Science for a pilot project providing $15 gift cards to patients who attend their scheduled appointments with physicians. They decided to forego a randomized control trial and provide gift cards to all patients who attended physician appointments for ethical reasons. They chose to conduct the pilot from April through June, as there would be fewer weather problems and holidays to inhibit attendance.  They also consulted the BMC legal team, who advised them that it was legal to provide monetary incentives to patients to promote access to care and that hospital policy stipulated the maximum amount to give is $15 per visit and $75 annually. Data collection was key to this intervention. A research assistant was hired to collect and analyze the data during the pilot, as well as assist the team in conducting interviews with both hospital stakeholders to learn their thoughts on the sustainability, feasibility, ethics, and acceptability of the intervention and also patients to hear about their experience with the intervention.",
"Workflow": "The typical hepatitis C clinic workflow: Patients initially are identified as hepatitis C patients in the BMC emergency department or specialty clinic. Once they are diagnosed, the team social worker is made aware and contacts patients to set up an appointment with a hepatitis C provider. They see a physician for an initial evaluation, during which mode of disease contraction, potential treatment, and level of motivation for treatment are discussed. They then receive outpatient testing to evaluate extent of disease (ultrasound and fibroscan of the liver), and they subsequently return to clinic to discuss test results and make the decision whether or not to treat. Typically, it takes a week or two for prior authorization to be approved (since 2016, all patients have been approved), at which time the patient meets with the clinical pharmacist to receive education around taking the drug and potential side effects/interactions, a calendar of treatment, and a prescription to receive the medication (if getting medication through BMC pharmacy, they receive their first bottle at the appointment). The clinical pharmacist calls the patient at week 2 and sees the patient in clinic at week 4 to take labs. 3 months after treatment, patients come to see the physician to check for cure and receive more education. The financial incentive pilot workflow: The social worker contacts the patient to set up an appointment with a physician and tells the patient that he or she will receive a $15 gift card at the appointment. When the patient arrives at the appointment, the physician gives the patient the gift card. For patients not seeing one of the four main hepatitis C physicians, the social worker gives the patient the gift card. Providing the gift card is included in the patient’s chart. Note: not all patients scheduled their appointments with the social worker, so a portion of patients who received the gift card at the appointment were unaware of it prior to attending the appointment.",
"Budget": "The pilot costed $14,000. This included $5,000 for the cost of the gift cards, the salary of a research assistant (helps with submitting paperwork, collecting and analyzing data)."}

global innovatorAll
innovatorsAll = {}
innovatorsAll['Cynthia So-Armah MD MPH'] = {"Name": 'Cynthia So-Armah MD MPH', "Bio": "Dr. Cynthia So-Armah is a primary care internist at Brookside Community Health Center in Jamaica Plain, MA. She also serves as lead physician for QI at Brookside, as well as assistant program director of QI for the Brigham and Women's Hospital internal medicine residency program. She is a graduate of UCSF medical school and completed her residency in primary care internal medicine at Brigham and Women's Hospital. Prior to pursuing medicine, she was a Latin American Studies major at Yale and co-founded a non-profit organization called Yspaniola that promotes quality education and full citizenship for Dominicans and Dominicans of Haitian descent living in bateys of the Dominican Republic."}
innovatorsAll['Jane Erb MD'] = {"Name": "Jane Erb MD", "Bio":"Having completed my residency training at UCLA Neuropsychiatric Institute in the late 1980s, I was immersed in an environment that emphasized integrating the mind with the brain through having been trained by clinicians and researchers who valued integrating psychoanalytic, cognitive-behavioral, social, and neuroscience models for understanding human behavior and treating mental illness from the start.  Largely because of my mentors, my training ran especially deep in eating and sleep disorders.  Consequently, I have always been attuned to and emphasized the basics of diet and sleep.  Over the years, I have acquired increasing psychopharmacologic expertise through my clinical practice, collaboration with those engaged in clinical trials, and teaching our resident psychiatrists.  In addition to my clinical and teaching activities, I have been working with BWH Population Health to build an integrated behavioral health program to care for the psychiatric needs of patients in the primary care setting.  My experience in that area began in 2011 when I became part of the South Huntington Advanced Primary Care practice to develop a model there.  Building upon my experience there and as an effort to address depression care where most of it already is being delivered, in Primary Care, I became involved in a Partners-wide project to develop a collaborative care program to assist Primary Care Practices throughout all Partners’ RSOs to integrate depression care into their daily workflow. Since then, I have worked closely with BWH Primary Care leadership to guide the roll out of collaborative care at all BWH practices and continue as a consulting psychiatrist now at 4 BWH practices.  It has been a joy to see clinicians providing more sophisticated psychiatric assessments, increasingly promoting non-pharmacologic interventions in managing their patients with milder illness, and encouraging the same in conjunction with Rx intervention for those with more severe depression. "}
# ensure responses aren't cached
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
    info = innovatorsAll[title]
    return render_template("intervention.html",title=title, info=info)
@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/profile")
def profile():
    return render_template("home.html")


@app.route("/team")
def team():
    return render_template("meetTheTeam.html")

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
    info = entries[title]
    return render_template("intervention.html",title=title, info=info)

@app.route("/search", methods=["GET", "POST"])
def search():
    """Enable user to buy a stock."""

    # POST
    if request.method == "POST":

        # validate form submission
        if not request.form.get("intervention"):
            return apology("missing intervention")
        ''' 
        elif not request.form.get("setting"):
            return apology("missing setting")
        elif not request.form.get("emrpref"):
            return apology("missing emr pref")
        elif not request.form.get("budget"):
            return apology("missing budget")'''
        
        results = []
        for k in entries:
            print('entries', entries[k]['Keywords'])
            print('term', request.form.get("intervention"))
            if request.form.get("intervention") in entries[k]['Keywords']:
                print('ya')
                results.append(entries[k])


        return render_template("results.html", results=results)


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
