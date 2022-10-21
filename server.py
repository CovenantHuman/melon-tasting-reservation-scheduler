"""Server for a melon tasting reservation scheduler web app."""

from flask import(Flask, render_template, request, flash, session, redirect)
from jinja2 import StrictUndefined
from model import connect_to_db, db
import crud
from datetime import datetime, timedelta

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


@app.route("/search-reservations", methods=["POST"])
def search_reservations():
    username = session.get("username")
    if username:
        date = request.form.get("date")
        start = request.form.get("start")
        if start == "":
            start = "00:00"
        end = request.form.get("end")
        if end == "":
            end = "00:00"
        dt_start_str = f"{date} {start}"
        dt_end_str = f"{date} {end}"
        dt_start = datetime.strptime(dt_start_str, '%Y-%m-%d %H:%M')
        dt_end = datetime.strptime(dt_end_str, '%Y-%m-%d %H:%M')
        if end == "00:00":
            dt_end += timedelta(days=1)
        user = crud.get_user_by_username(username)
        reservations = user.reservations
        date_conflict = False
        for reservation in reservations:
            if reservation.datetime.date() == dt_start.date():
                date_conflict = True
        if date_conflict:
            flash(f"{username} already has an appointment on {dt_start.date()}. Cannot make more than one reservation per day.")
            return redirect("/search-reservations")
        else:
            appts_start = dt_start + (datetime.min - dt_start) % timedelta(minutes=30)
            appts_end = dt_end - (dt_end - datetime.min) % timedelta(minutes=30)
            appt_times = []
            current = appts_start
            while current < appts_end:
                if not crud.get_reservation_by_datetime(current):
                    appt_times.append(current)
                current += timedelta(minutes=30) 
            flash(f"{appts_start} {appts_end} {appt_times}")
            return render_template("search_results.html", appt_times=appt_times)
    else:
        return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    
    app.run(host="0.0.0.0", debug=True)


