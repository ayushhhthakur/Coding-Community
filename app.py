from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connect to the database
db = mysql.connector.connect(
    host="hostname",
    user="username",
    password="password",
    database="database_name"
)
@app.route("/")
def index():
    # Get the search term from the query string
    search_term = request.args.get("search")
    
    # Query the database based on the search term
    cursor = db.cursor()
    if search_term:
        cursor.execute("SELECT * FROM user_profiles WHERE skill LIKE %s", ('%' + search_term + '%',))
    else:
        cursor.execute("SELECT * FROM user_profiles")
    data = cursor.fetchall()
    return render_template("index.html", data=data)

@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        # Get the form data
        username = request.form["username"]
        email = request.form["email"]
        skill = request.form["skill"]
        city = request.form["city"]

        # Check if email already exists in database
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_profiles WHERE email = %s", (email,))
        if cursor.fetchone()[0] > 0:
            email_error = 'Email already exists. Please enter a different email address.'
            return render_template("add_user.html", email_error=email_error)

        # Insert into the database
        cursor.execute("INSERT INTO user_profiles (username, email, skill, city) VALUES (%s, %s, %s, %s)", (username, email, skill, city))
        db.commit()

        return redirect("/")
    else:
        return render_template("add_user.html")

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route("/check_email/<email>")
def check_email(email):
    user = user.query.filter_by(email=email).first()
    if user:
        return "exists"
    else:
        return ""

if __name__ == "__main__":
    app.run(debug=True)
