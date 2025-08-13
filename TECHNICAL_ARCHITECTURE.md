# Technical Architecture

**Stack**: Streamlit (UI+logic), Python, OpenAI SDK (optional), APScheduler, CSV storage.

```
+-----------------------+
|   Streamlit (UI)      |
|  - Pages (4)          |
|  - User actions       |
+-----------+-----------+
            |
            v
+-----------+-----------+
|  Utils (services)     |
|  - ai.py (OpenAI/off) |
|  - storage.py (CSV)   |
|  - scheduler.py       |
|  - safety.py          |
+-----------+-----------+
            |
            v
+-----------+-----------+
|    data/*.csv         |
|  profiles, ideas,     |
|  posts, schedules,    |
|  analytics            |
+-----------------------+
```

**Scheduler**: On each app run and via a small APScheduler job, we check due posts and mark them posted, then generate simulated analytics.

**Security**: No external tokens stored. If `OPENAI_API_KEY` is present, it resides in the process env only.
