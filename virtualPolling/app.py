import os
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session



db =SQL("sqlite:///users.db")


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)




@app.route("/",methods=["GET", "POST"])
def index():
    if not session.get("name"):
        return redirect("/login")
    return render_template("index.html")




@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if not email:
            return render_template("error.html", message = "email not found")
        elif not password:
            return render_template("error.html",message = "password not found")


        cemail = db.execute("Select email FROM users WHERE email = ? "
        ,request.form.get("email"))
        cpass = db.execute("SELECT password FROM users WHERE email = ?"
        ,request.form.get("email"))

        if len(cemail) != 1 or len(cpass) != 1:
            return render_template("error.html",message ="user or password is incorrect")

        session["name"] = request.form.get("email")
        return render_template("index.html")




    return render_template("login.html")


@app.route("/register",methods =["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            return render_template("error.html", message = "email not found")
        first = request.form.get("firstname")
        if not first:
            return render_template("error.html",message="First name missing")
        last = request.form.get("lastname")
        if not last:
            return render_template("error.html",message="Last name missing")
        userid = request.form.get("userid")
        if not userid:
            return render_template("error.html",message ="userid")

        password =request.form.get("password")
        if not password:
            return render_template("error.html",message="password missing")
        conform = request.form.get("Re-password")
        if not conform:
            return render_template("error.html",message="Re-password missing")
        if password != conform:
            return render_template("error.html",message="password didn't matched")

        db.execute("INSERT INTO users (lastname, firstname, email,userid,password) VALUES(?, ?,?,?,?)"
        , last, first,email,userid,password)


        return render_template("login.html")

    return render_template("regester.html")


@app.route("/pre",methods =["GET", "POST"])
def pre():
    if request.method == "POST":
        sag = request.form.get("sag")
        catagory = request.form.get("category")
        db.execute("INSERT INTO SAG (user_id,games,catagory) VALUES( ?,?,?)",
        session.get("name"), sag, catagory)

        return render_template("thank.html")
    else:
        return render_template("index.html")


@app.route("/registrents")
def registrents():
    games = db.execute("SELECT * FROM SAG WHERE user_id IS ?",session.get("name"))
    return render_template("registrents.html",games=games)



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")