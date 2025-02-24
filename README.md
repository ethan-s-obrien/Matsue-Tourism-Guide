# Matsue Tourism Guide

## Video Demo: <URL HERE>

## Description: 

**Matsue Tourism Guide** is a web application designed as my **final project for CS50**, aimed at helping visitors discover **tourist spots in and around Matsue, Japan**. The app provides **personalized itinerary recommendations** based on user preferences, leveraging **Flask for the backend, SQLite for database management, and Bootstrap for a responsive frontend**.

Users create an account, complete a **custom survey** about their trip, and receive a dynamically generated itinerary that **prioritizes locations based on their interests and trip duration**. The scoring system incorporates **user preferences and location popularity ratings**, the latter informed by my own experience working in the Matsue tourism industry.

This project represents my **first full-stack web application**, integrating **Python, JavaScript, HTML, and CSS**, and serving as a milestone in my development journey.

---

## 🎯 Features

✅ **User Authentication & Persistent Itineraries**

- Secure **user registration & login**, with passwords stored as **secure hashes**.
- The latest **submitted survey determines the user's itinerary**, without overwriting previous data.

✅ **Personalized Itinerary Generation**

- Users complete a survey to **rank their interests** in different types of attractions.
- Locations are assigned scores based on **preferences & popularity**.
- **Trip duration & sightseeing pace** determine the number of activities per day.

✅ **Dynamic Travel Timeline**

- **Bootstrap cards** display attractions in a **scrollable itinerary format**.
- Each card contains an **image, description, opening hours, homepage link, and a Google Maps link**.
- Cards are **divided into Morning & Afternoon sections** for each day.

✅ **Draggable Preferences Ranking**

- The survey includes a **draggable list** for ranking attraction types.
- Implemented via **JavaScript & CSS** for an intuitive user experience.

✅ **See More Button for Cleaner UI**

- Attraction descriptions are truncated until **"See More"** is clicked.
- Expands the card dynamically while keeping initial layout **uniform & structured**.

✅ **Retake Survey Without Losing Data**

- Users can **retake the survey** as many times as they like.
- **All previous survey responses are stored**, but only the latest submission is used to generate the itinerary.

✅ **Mobile-Friendly & Responsive Design**

- **Bootstrap-powered UI** ensures usability across **desktop & mobile**.

---

## 🏗️ Project Structure

📂 **Matsue-Tourism-Guide/** _(Root Directory)_  
📄 **App.py** – The main Flask application, handling **user authentication, survey processing, itinerary generation, and database interactions**.

📂 **templates/** _(HTML Templates for Jinja Rendering)_

- **layout.html** – Base template extended by all other pages.
- **index.html** – Home page introduction.
- **register.html / login.html** – User authentication pages.
- **survey.html** – The user survey form with **draggable preference ranking**.
- **mytrip.html** – The generated **custom itinerary page**.
- **error.html** – Displays the error messages.

📂 **static/** _(CSS, JavaScript, and Images)_

- **styles.css** – Custom styling for the web app.
- **images** – Images used for **tourist spots cards**and **the landing page carousel**.

📂 **instance/** _(SQLite Database)_

- **database.db** – Stores user accounts, survey responses, and tourist location data.

📂 **Tourism-Spots/** _(CSV Import Files)_

- **Tourism_Spots.csv** – The dataset containing all **tourist spots, categories, durations, and popularity ratings**.

---

## ⚙️ How It Works

### 📝 **Survey & Itinerary Generation**

1. **User registers & logs in**.
2. **User completes the survey**, ranking their **preferred attraction types**.
3. **Survey data is stored**, with each preference assigned a **score based on ranking order**.
4. **Tourist spots are scored** based on **user preference & popularity**.
5. **The itinerary is generated**, structured by **days & sessions (morning/afternoon)**.

### 🖥️ **Backend Logic (Flask & SQLite)**

- **Session-based authentication** keeps track of logged-in users.
- **User-submitted surveys are stored** via foreign keys linking responses to users.
- **Survey responses dynamically determine itinerary generation**.

### 🎨 **Frontend (Bootstrap & JavaScript)**

- **Itinerary displayed as a vertical timeline**, with **cards connected by a line**.
- **Cards are interactive**, with **expandable descriptions** and **draggable preference rankings**.
- **Google Maps links auto-generate** from location coordinates.

---

## 🔍 Design Decisions

### 1️⃣ **Draggable Ranking vs. Dropdowns**

Initially, I considered **dropdown selections** for user preferences, but a **drag-and-drop ranking** was more intuitive. Implementing it required **JavaScript for interactivity** and **CSS for styling**.

### 2️⃣ **Why Save All Surveys?**

Instead of overwriting old survey data, each survey is stored **separately**. This prevents accidental data loss while allowing users to **recreate past itineraries**.

### 3️⃣ **Why a Timeline Format?**

Rather than a **simple list**, I chose a **vertical timeline layout**. This makes the itinerary more **readable and structured**, clearly dividing **morning & afternoon** activities.

### 4️⃣ **Keeping UI Clean with “See More”**

Instead of **showing all details upfront**, the **See More button** keeps cards **uniform**. Expanding a card **adjusts the image size dynamically** without distortion.

---

## 🚀 Lessons Learned

✅ **Database Design is Crucial** – Early issues with survey storage reinforced the importance of **well-structured database relationships**.

✅ **Debugging SQL Queries & Jinja** – Extracting & processing survey responses properly required understanding **fetchall vs. fetchone**, list handling, and **foreign key relationships**.

✅ **Full-Stack Integration** – This project strengthened my **Flask, Jinja, Bootstrap, and JavaScript** skills, giving me experience in **frontend-backend interaction**.

✅ **CSS Layout Challenges** – Creating a **structured timeline with expandable cards** required careful CSS handling, particularly in **image resizing and responsive layout**.

✅ **Iterative Problem-Solving** – Many features evolved through **trial and error**, debugging, and **restructuring approaches** for better efficiency.

---

## 🛠️ Future Improvements

🔹 **Drag-and-Drop Itinerary Adjustments** – Allow users to **rearrange itinerary items** interactively.

🔹 **Google Maps Integration** – Display **selected attractions on a dynamic map**.

🔹 **Printable & Shareable Itineraries** – Enable users to **export or share their trip plan** with others.

🔹 **Return to Previous Itinerary** – Add a feature to go back to a previously generated itinerary.

🔹 **Improved UI** – Further refine layout and add animations on landing page and itinerary page.

---

## 💡 Final Thoughts

This project represents **version 1** of my vision for the **Matsue Tourism Guide**. The development process has been a **valuable learning experience**, reinforcing my skills in **full-stack web development, database design, and user experience optimization**.

Moving forward, I plan to **continue expanding the app** by integrating new features and improving the **user interface** based on real-world usability testing. 🚀

---

## 📜 Credits & Acknowledgments

This project was designed, built, and developed by **Ethan O'Brien**.

During development, I used:

- **w3schools.com** for syntax references.
- **Bootstrap's documentation** for styling & responsive design.
- **ChatGPT** as a **debugging assistant & brainstorming partner**, particularly for refining implementation strategies.

All **architecture, coding decisions, problem-solving, and debugging** were **done independently by me**, with AI tools serving only as an **advisory resource**.
