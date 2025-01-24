import os
import sqlite3

from flask import Flask, g, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['DATABASE'] = os.path.join(app.instance_path, 'database.db')
os.makedirs(app.instance_path, exist_ok=True)


def get_db():
    """Connect to the database."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

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
        user_id = session.get('user_id')
        travel_mode = request.form.get('travel_mode')
        group_size = request.form.get('group_size')
        days = int(request.form.get('hours'))
        country = request.form.get('country')
        preferences = request.form.get('preferences').split(',') # Converts CSV to a list
        age_brackets = {
            '0-9': int(request.form.get('age_0_9', 0)),
            '10-19': int(request.form.get('age_10_19', 0)),
            '20-29': int(request.form.get('age_20_29', 0)),
            '30-39': int(request.form.get('age_30_39', 0)),
            '40-49': int(request.form.get('age_40_49', 0)),
            '50-59': int(request.form.get('age_50_59', 0)),
            '60-69': int(request.form.get('age_60_69', 0)),
            '70+': int(request.form.get('age_70+', 0)),
        }

        # Save survey responses
        conn = get_db()
        try: 
            # Insert survey response
            response_id = conn.execute(
                "INSERT INTO SurveyResponses (user_id) VALUES (?)", (user_id,)
            ).lastrowid

            # Insert preferences
            for rank, category in enumerate(preferences, start=1):
                conn.execute(
                    "INSERT INTO Preferences (response_id, preference, rank) VALUES (?,?,?)",
                    (response_id, category, rank)
                )
            
            # Insert trip length
            conn.execute(
                "INSERT INTO TripLength (response_id, days, hours) VALUES (?,?,?)",
                (response_id, days, hours)
            )

            # Insert age brackets
            for bracket, count, in age_brackets.items():
                if count > 0: # Only save non-zero brackets
                    conn.execute(
                        "INSERT INTO AgeBrackets (response_id, age_bracket, num_people) VALUES (?, ?, ?)",
                        (response_id, bracket, count)
                    )

            # Commit changes
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error saving survey data: {e}")
            return "An error occurred while saving your survey data.", 500

        # Redirect to the next step
        return redirect('/mytrip')
    
    # Render form for GET requests
    return render_template('survey.html')