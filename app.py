from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)

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

@app.route("/")
def login():
    return render_template("login.html")

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
    return render_template("welcome.html")



app.run(debug=True)