from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
app = Flask(__name__)
app.secret_key = "Shifah"

def connect_db():
    return sqlite3.connect("users.db")

#create a table
def create_table():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        create table if not exists Users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   username TEXT,
                   email TEXT,
                   password varchar (20));
    """)
    db.commit()
    db.close()

create_table()

@app.route("/", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users WHERE username=? AND password=?", (username, password))
        account = cursor.fetchone()
        db.close()
        if account:
            session["username"] = username
            return redirect(url_for("welcome"))
        else:
            msg = "Invalid username or password"
    return render_template("login.html", msg = msg)

@app.route("/register", methods=["GET", "POST"])
def register():
    msg = "" 
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
        account = cursor.fetchone()
        if account: 
            msg = "Account already exists."
        else:
            cursor.execute("INSERT INTO Users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
            db.commit()
            msg = "Registration Successful!"
        db.close()
    return render_template("register.html", msg = msg)

@app.route("/welcome")
def welcome():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("welcome.html", username = session["username"])



app.run(debug=True)