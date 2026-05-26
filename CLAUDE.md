# StudyPulse — CLAUDE.md

## What this is
A Flask web app for logging study sessions and tracking weekly progress.
Students add sessions (subject, duration, mood), see a weekly bar chart,
and get a streak counter for consecutive days studied.

## Stack
- Python 3 + Flask
- In-memory storage only — no database, no SQLAlchemy
- Jinja2 templates
- pytest for tests
- werkzeug for any auth if added later

## Data shape
A session is a dict:
```python
{
    "subject": "Math",
    "duration_minutes": 45,
    "mood": "focused",   # one of: focused, distracted, tired
    "date": "2026-05-26" # ISO string, always today's date
}
```
All sessions live in a module-level list in `app.py`: `sessions = []`

## Conventions
- Helpers (weekly_summary, streak_count, add_session) live in `helpers.py`
- Templates in `templates/`
- Tests in `tests/` — one file per feature area
- Never store plaintext secrets; no API keys in source

## Out of scope (do not add unless explicitly asked)
- Database or file persistence
- User accounts or login
- JavaScript frameworks
- Email or notifications
- Mobile app