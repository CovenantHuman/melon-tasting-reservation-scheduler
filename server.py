"""Server for a melon tasting reservation scheduler web app."""

from flask import(Flask, render_template, request, flash, session, redirect)
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def show_login_page():
    """Display the login page"""
    return render_template("login.html")

@app.route("/login-user", methods=["POST"])
def login_user():
    """Login the user"""
    username = request.form.get("username")
    session['username'] = username
    flash('Logged in!')
    return redirect("/reservation-search")

if __name__ == "__main__":
    # connect_to_db(app)
    
    app.run(host="0.0.0.0", debug=True)