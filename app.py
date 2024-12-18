from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "ctf_secret_key"

#  database
users = {"admin": "admin123", "user": "user123"}
paths = ["/about", "/contact", "/hidden_clue"]

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Vulnerable SQL-like authentication
        if username in users and password == users[username]:
            session["user"] = username
            return redirect("/admin" if username == "admin" else "/user")
        return render_template("login.html", error="Invalid credentials. Try again!")

    return render_template("login.html")

@app.route("/admin")
def admin():
    if session.get("user") == "admin":
        return render_template("admin.html", flag="CTF{Advanced_Multi_Page_Bypass}")
    return render_template("fake_dashboard.html")

@app.route("/user")
def user():
    if session.get("user"):
        return render_template("user.html", username=session["user"])
    return redirect("/")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/hidden_clue")
def hidden_clue():
    return render_template("hidden_clue.html", clue="Look deeper into session tokens!")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
