"""Server for a melon tasting reservation scheduler web app."""

from flask import(Flask, render_template, request, flash, session, redirect)
from jinja2 import StrictUndefined
from model import connect_to_db
import crud

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
    user = crud.get_user_by_username(username)
    if user: 
        session['username'] = username
        flash('Logged in!')
        return redirect("/reservation-search")
    else:
        flash('Not logged in!')
        return redirect("/")

@app.route("/reservation-search")
def show_reservation_search_page():
    if session.get("username"):
        return render_template('appointment_search.html')
    else:
        return redirect("/")

if __name__ == "__main__":
    connect_to_db(app)
    
    app.run(host="0.0.0.0", debug=True)


