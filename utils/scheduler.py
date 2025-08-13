import datetime as dt, pandas as pd, numpy as np, random, pytz
from .storage import read, write, mark_posted, add_analytics

def run_due_jobs():
    schedules = read("schedules")
    if schedules.empty: return 0
    now = dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)
    posts = read("posts")
    count=0
    for _, row in schedules.iterrows():
        when = dt.datetime.fromisoformat(row["scheduled_at"].replace("Z","+00:00"))
        if when <= now:
            post_id = row["post_id"]
            # Mark as posted
            mark_posted(post_id, external_id=None)
            # Simulated analytics
            base = random.randint(500, 4000)
            reactions = max(5, int(base * random.uniform(0.01, 0.05)))
            comments = max(1, int(reactions * random.uniform(0.05, 0.2)))
            add_analytics(post_id, base, reactions, comments)
            count+=1
    # Remove executed schedules
    remaining = schedules[schedules["scheduled_at"] > now.isoformat()]
    write("schedules", remaining)
    return count
