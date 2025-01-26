CREATE TABLE Users (
user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
username TEXT NOT NULL, 
email TEXT NOT NULL,
hash TEXT NOT NULL
);

CREATE TABLE SurveyResponses ( 
response_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
user_id INTEGER NOT NULL, 
submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Answers (
answer_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
response_id INTEGER,
question TEXT,
answer TEXT,
FOREIGN KEY (response_id) REFERENCES SurveyResponses(response_id)
);

CREATE TABLE TripLength (
time_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
response_id INTEGER,
days INTEGER,
hours INTEGER,
FOREIGN KEY (response_id) REFERENCES SurveyResponses(response_id)
);

CREATE TABLE AgeBrackets (
age_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
response_id INTEGER,
age_bracket TEXT,
num_people INTEGER,
FOREIGN KEY (response_id) REFERENCES SurveyResponses(response_id)
);

CREATE TABLE Preferences (
preference_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
response_id INTEGER,
rank INTEGER,
preference TEXT,
FOREIGN KEY (response_id) REFERENCES SurveyResponses(response_id)
);

CREATE TABLE TouristSpots (
spot_id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
category TEXT NOT NULL,  -- e.g., 'historical', 'cultural', 'natural'
description TEXT,
image_url TEXT,
homepage TEXT,
latitude REAL,
longitude REAL,
open_hours TEXT,
duration TEXT,
popularity INTEGER
);
