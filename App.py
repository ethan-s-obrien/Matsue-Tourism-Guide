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

app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'database.db')
os.makedirs(app.instance_path, exist_ok=True)


def get_db():
    """Connect to the database."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row # Enable dictionary-like row access
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

    conn = get_db()

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="You must provide username."), 400

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message="You must provide password."), 400

        # Query database for username
        rows = conn.execute(
            "SELECT * FROM Users WHERE username = ?", (request.form.get("username"),)
        ).fetchall() # Fetch all the matching rows as a list

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("error.html", message="Invalid username and/or password."), 400

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Check if user has submitted their survey
        survey_check = conn.execute(
            "SELECT COUNT(*) FROM SurveyResponses WHERE user_id = ?", (rows[0]["user_id"],)
        ).fetchone()[0]

        # Redirect to survey if none found
        if survey_check == 0:
            return redirect("/survey")


        # Redirect user to home page
        return redirect("/mytrip")

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

        conn = get_db()

        # Username & Password registration
        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate registration
        if not name:
            return render_template("error.html", message="You must provide a name."), 400
        elif not password:
            return render_template("error.html", message="Missing password."), 400
        elif password != confirmation:
            return render_template("error.html", message="Passwords did not match."), 400

        # Check if username already exists
        sql_count = conn.execute("SELECT COUNT(*) AS count FROM users WHERE username = ?", (name,))
        username_count = sql_count.fetchone()[0] # Fetchone to check username isn't in use
        if username_count != 0:
            return render_template("error.html", message="Username already exists."), 400

        # Hash password
        hashed_password = generate_password_hash(password)

        # Insertion of valid registration into database and fetch user_id for automatic login following registration
        cursor = conn.execute("INSERT INTO users (username, email, hash) VALUES(?, ?, ?)", (name, email, hashed_password))
        conn.commit()
        session["user_id"] = cursor.lastrowid

        # Redirect on success
        return redirect("/survey")

    # Render registration page for GET
    return render_template("register.html")

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':

        # Collect user ID from session
        user_id = session.get('user_id')
        conn = get_db()

        # Collect form data
        travel_mode = request.form.get('travel_mode')
        group_size = request.form.get('group_size')
        days = int(request.form.get('days'))
        hours = int(request.form.get('hours'))
        country = request.form.get('country')
        preferences = request.form.get('preferences')
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


        # Insert survey responses
        try: 
            # Insert survey response
            response_id = conn.execute(
                "INSERT INTO SurveyResponses (user_id) VALUES (?)", (user_id,)
            ).lastrowid

            # Prepare questions and answers for the Answers table
            questions_and_answers = [
                ("How will you travel to Matsue?", travel_mode),
                ("How many people in your group?", group_size),
                ("How long do you plan to stay?", f"{days} days, {hours} hours"),
                ("What country are you from?", country),
                ("Rank your preferences", ', '.join(preferences)), #Join preferences as a string
            ]

            # Add age-bracket data as additional question-answer pairs
            for bracket, count in age_brackets.items():
                if count > 0:
                    questions_and_answers.append((f"Number of people aged {bracket}", str(count)))

            # Insert all questions and answers into the Answers table
            conn.executemany(
                "INSERT INTO Answers (response_id, question, answer) VALUES (?, ?, ?)",
                [(response_id, question, answer) for question, answer in questions_and_answers]
            )

            # Insert preferences
            conn.execute(
                "INSERT INTO Preferences (response_id, preference) VALUES (?,?)",
                (response_id, preferences)
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
    return render_template('survey.html', on_survey=True)

@app.route('/mytrip')
def generate_itinerary():
    """Generate the personalized itinerary for the user"""
    conn = get_db()

    # Get the current user ID from the session
    user_id = session.get('user_id')
    if not user_id:
        return render_template("error.html", message="You must be logged in to view your trip."), 403
    
    # Fetch the latest survey data submitted
    latest_response = conn.execute("""
        SELECT response_id
        FROM SurveyResponses
        WHERE user_id = ?
        ORDER BY submitted_at DESC
        LIMIT 1
    """, (user_id,)).fetchone()

    # Ensure we actually pulled survey data
    if not latest_response:
        return render_template("error.html", message="No survey found. Please complete the survey first."), 400
    
    # Use the latest survey response_id for the user
    response_id = latest_response['response_id']

    #Fetch user data via response_id
    user_preferences = conn.execute("""
        SELECT preference
        FROM Preferences
        WHERE response_id = ?
    """, (response_id,)).fetchone()

    # Ensure there's a valid result before processing
    preferences_list = user_preferences[0].split(',')  # Correctly split CSV string

    preferences = {category.strip(): len(preferences_list) - index for index, category in enumerate(preferences_list)}
    
    # Debugging check
    print(f"Processed Preferences: {preferences}")

    trip_length = conn.execute("""
    SELECT days, hours
    FROM TripLength
    WHERE response_id = ?                     
    """, (response_id,)).fetchone()

    # Calculate total trip time in hours
    total_time = trip_length['days'] * 7 + trip_length['hours'] # Total hours of trip based on 7 hours of sightseeing per day

    all_spots = conn.execute("""
        SELECT name, category, description, image_url, homepage, latitude, longitude, open_hours, duration_hours, popularity
        FROM TouristSpots
    """).fetchall()

    # Step 2: Score and filter spots
    scored_spots = []
    for spot in all_spots:
        # Category scoring
        category_score = preferences.get(spot['category'], 0) # Default low score if not in preferences
        # Calculate popularity score
        popularity_score = spot['popularity']
        # Final Score
        final_score = category_score + popularity_score
        
        print(f"Spot: {spot['name']}, Category: {spot['category']}, "
          f"Category Score: {category_score}, Popularity Score: {popularity_score}, Final Score: {final_score}")
        # Add spot details and scores
        scored_spots.append({
            'spot': spot,
            'score': final_score,
            'visit_duration': (spot['duration_hours'])
        })
 
    # Step 3: Sort by score descending
    scored_spots = sorted(scored_spots, key=lambda x: x['score'], reverse=True)

    # Step 4: Build the itinerary
    itinerary = []
    remaining_time = total_time
    for spot_data in scored_spots:
        if spot_data in scored_spots:
            if spot_data['visit_duration'] <= remaining_time:
                itinerary.append(spot_data['spot'])
                remaining_time -= spot_data['visit_duration']

            if remaining_time <= 0: # Beak loop no time left
                break

    # Step 5: Divide trip schedule into days with mornings and afternoons
    current_day = 1
    morning_count = 0
    afternoon_count = 0
    structured_itinerary = {}

    for spot_data in scored_spots:
        if current_day not in structured_itinerary:
            structured_itinerary[current_day] = []

        spot = dict(spot_data['spot']) # Feed in all the data to structured_itinerary
        visit_duration = spot_data['visit_duration']

        if morning_count < 2:
            spot['time_of_day'] = "Morning"
            structured_itinerary[current_day].append(spot)
            morning_count += 1
        elif afternoon_count < 3:
            spot['time_of_day'] = "Afternoon"
            structured_itinerary[current_day].append(spot)
            afternoon_count += 1
        else:
            current_day += 1
            morning_count = 0
            afternoon_count = 0

    
    return render_template("mytrip.html", itinerary=structured_itinerary)
