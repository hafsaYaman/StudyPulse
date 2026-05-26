from flask import Flask, render_template, request, redirect, url_for
from helpers import add_session, weekly_summary, streak_count
 
app = Flask(__name__)
 
sessions = []
 
@app.route("/")
def index():
    summary = weekly_summary(sessions)
    streak = streak_count(sessions)
    return render_template("index.html", sessions=sessions, summary=summary, streak=streak)
 
@app.route("/add", methods=["GET", "POST"])
def add():
    error = None
    if request.method == "POST":
        subject = request.form.get("subject", "").strip()
        duration = request.form.get("duration_minutes", "").strip()
        mood = request.form.get("mood", "").strip()
        try:
            add_session(sessions, subject, int(duration), mood)
            return redirect(url_for("index"))
        except ValueError as e:
            error = str(e)
    return render_template("add.html", error=error)
 
if __name__ == "__main__":
    app.run(debug=True)
