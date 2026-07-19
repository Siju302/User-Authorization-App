from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")



app.run(debug=True)