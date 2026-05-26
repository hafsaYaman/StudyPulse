import pytest
from datetime import date, timedelta
from helpers import add_session, weekly_summary, streak_count


# --- add_session ---

def test_add_session_valid():
    sessions = []
    add_session(sessions, "Math", 45, "focused")
    assert len(sessions) == 1
    assert sessions[0]["subject"] == "Math"
    assert sessions[0]["duration_minutes"] == 45
    assert sessions[0]["mood"] == "focused"
    assert sessions[0]["date"] == date.today().isoformat()

def test_add_session_empty_subject():
    with pytest.raises(ValueError):
        add_session([], "", 30, "focused")

def test_add_session_zero_duration():
    with pytest.raises(ValueError):
        add_session([], "Math", 0, "focused")

def test_add_session_invalid_mood():
    with pytest.raises(ValueError):
        add_session([], "Math", 30, "happy")


# --- weekly_summary ---

def test_weekly_summary_empty():
    assert weekly_summary([]) == {}

def test_weekly_summary_groups_by_subject():
    sessions = [
        {"subject": "Math", "duration_minutes": 30, "mood": "focused", "date": date.today().isoformat()},
        {"subject": "Math", "duration_minutes": 20, "mood": "tired", "date": date.today().isoformat()},
        {"subject": "English", "duration_minutes": 40, "mood": "focused", "date": date.today().isoformat()},
    ]
    summary = weekly_summary(sessions)
    assert summary["Math"] == 50
    assert summary["English"] == 40


# --- streak_count ---

def test_streak_empty():
    assert streak_count([]) == 0

def test_streak_today_only():
    sessions = [{"date": date.today().isoformat()}]
    assert streak_count(sessions) == 1

def test_streak_consecutive_days():
    today = date.today()
    sessions = [
        {"date": today.isoformat()},
        {"date": (today - timedelta(days=1)).isoformat()},
        {"date": (today - timedelta(days=2)).isoformat()},
    ]
    assert streak_count(sessions) == 3

def test_streak_gap_breaks_streak():
    today = date.today()
    sessions = [
        {"date": today.isoformat()},
        {"date": (today - timedelta(days=2)).isoformat()},  # gap on day 1
    ]
    assert streak_count(sessions) == 1