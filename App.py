import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

if __name__ == '__main__':
    app.run(debug=True)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
     return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("mytrip.html")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == 'POST':

        # Username & Password registration
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate registration
        if not name:
            return apology("Missing Username", 400)
        elif not password:
            return apology("Missing Password", 400)
        elif password != confirmation:
            return apology("Password's did not match", 400)

        # Check if username already exists
        sql_count = db.execute("SELECT COUNT(*) AS count FROM users WHERE username = ?", name)
        username_count = sql_count[0]["count"]
        if username_count != 0:
            return apology("Username already exists", 400)

        # Hash password
        hashed_password = generate_password_hash(password)

        # Insertion of valid registration into database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", name, hashed_password)

        # session['user_id'] = new_user.id #Have new user be logged in

        # Redirect on success
        return redirect("/survey")

    # Render registration page for GET
    return render_template("register.html")

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        #Process survey data
        pref_1 = request.form.get('1st_pref')
        user_id = session.get('user_id')
        return redirect('/mytrip')
    return render_template('survey.html')