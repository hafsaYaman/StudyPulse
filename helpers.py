from datetime import date, timedelta
 
VALID_MOODS = {"focused", "distracted", "tired"}
 
 
def add_session(sessions, subject, duration_minutes, mood):
    if not subject:
        raise ValueError("Subject cannot be empty.")
    if duration_minutes <= 0:
        raise ValueError("Duration must be greater than zero.")
    if mood not in VALID_MOODS:
        raise ValueError(f"Mood must be one of: {', '.join(VALID_MOODS)}.")
    sessions.append({
        "subject": subject,
        "duration_minutes": duration_minutes,
        "mood": mood,
        "date": date.today().isoformat(),
    })
 
 
def weekly_summary(sessions):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())  # Monday
    totals = {}
    for s in sessions:
        if s["date"] >= week_start.isoformat():
            totals[s["subject"]] = totals.get(s["subject"], 0) + s["duration_minutes"]
    return totals
 
 
def streak_count(sessions):
    if not sessions:
        return 0
    logged_dates = {s["date"] for s in sessions}
    streak = 0
    check = date.today()
    while check.isoformat() in logged_dates:
        streak += 1
        check -= timedelta(days=1)
    return streak
 
