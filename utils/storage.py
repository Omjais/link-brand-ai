import os, pandas as pd, datetime as dt, uuid

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

def _path(name: str) -> str:
    return os.path.join(DATA_DIR, f"{name}.csv")

def _ensure(name: str, cols: list[str]):
    p = _path(name)
    if not os.path.exists(p):
        pd.DataFrame(columns=cols).to_csv(p, index=False)

def read(name: str) -> pd.DataFrame:
    p = _path(name)
    if not os.path.exists(p):
        return pd.DataFrame()
    return pd.read_csv(p)

def write(name: str, df: pd.DataFrame):
    df.to_csv(_path(name), index=False)

def add_profile(raw_text: str, voice_json: dict) -> str:
    _ensure("profiles", ["id","created_at","raw","voice","pillars","pitch"])
    df = read("profiles")
    pid = str(uuid.uuid4())
    row = {
        "id": pid,
        "created_at": dt.datetime.utcnow().isoformat(),
        "raw": raw_text,
        "voice": str(voice_json.get("voice")),
        "pillars": ",".join(voice_json.get("pillars", [])),
        "pitch": voice_json.get("pitch","")
    }
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    write("profiles", df)
    return pid

def add_ideas(profile_id: str, ideas: list[dict]):
    _ensure("ideas", ["id","profile_id","created_at","title","angle","cta"])
    df = read("ideas")
    rows=[]
    for idea in ideas:
        rows.append({
            "id": str(uuid.uuid4()),
            "profile_id": profile_id,
            "created_at": dt.datetime.utcnow().isoformat(),
            "title": idea.get("title",""),
            "angle": idea.get("angle",""),
            "cta": idea.get("suggested_CTA","")
        })
    df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
    write("ideas", df)

def add_post(profile_id: str, idea_title: str, variant: str, text: str, hashtags: list[str]) -> str:
    _ensure("posts", ["id","profile_id","created_at","idea_title","variant","text","hashtags","status"])
    df = read("posts")
    pid = str(uuid.uuid4())
    row = {
        "id": pid,
        "profile_id": profile_id,
        "created_at": dt.datetime.utcnow().isoformat(),
        "idea_title": idea_title,
        "variant": variant,
        "text": text,
        "hashtags": ",".join(hashtags),
        "status": "draft"
    }
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    write("posts", df)
    return pid

def schedule_post(post_id: str, when_iso: str, tz: str="UTC"):
    _ensure("schedules", ["id","post_id","scheduled_at","timezone","result"])
    df = read("schedules")
    row = {
        "id": str(uuid.uuid4()),
        "post_id": post_id,
        "scheduled_at": when_iso,
        "timezone": tz,
        "result": ""
    }
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    write("schedules", df)

def mark_posted(post_id: str, external_id: str|None):
    df = read("posts")
    if df.empty: return
    df.loc[df["id"]==post_id, "status"] = "posted"
    write("posts", df)

def add_analytics(post_id: str, impressions: int, reactions: int, comments: int):
    _ensure("analytics", ["id","post_id","collected_at","impressions","reactions","comments"])
    df = read("analytics")
    row = {
        "id": str(uuid.uuid4()),
        "post_id": post_id,
        "collected_at": dt.datetime.utcnow().isoformat(),
        "impressions": impressions,
        "reactions": reactions,
        "comments": comments
    }
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    write("analytics", df)
