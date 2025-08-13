import os, json, random
from dataclasses import dataclass

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

@dataclass
class Voice:
    voice: dict
    pillars: list[str]
    pitch: str

def _offline_voice(text: str) -> Voice:
    return Voice(
        voice={"tone":"helpful","energy":"medium","formality":"semi-formal","emoji_policy":"sparingly"},
        pillars=["Lessons learned","Industry trends","How-to tips"],
        pitch="Builder sharing practical lessons to help others move faster."
    )

def _offline_ideas() -> list[dict]:
    titles = [
        "3 mistakes I made last year",
        "A tiny habit that 10x'd my output",
        "What newcomers misunderstand about our industry",
        "A simple framework I use weekly",
        "The toolchain I recommend in 2025"
    ]
    out=[]
    for t in titles:
        out.append({"title": t, "angle": "Personal insight + actionable takeaways",
                    "why_it_matters": "Helps your audience avoid pitfalls",
                    "suggested_CTA": "What would you add?"})
    return out

def _offline_posts(idea_title: str) -> dict:
    A = f"{idea_title}: Here are 3 lessons that saved me weeks...\n- Lesson 1\n- Lesson 2\n- Lesson 3\nCTA: What would you add?"
    B = f"Hook: I learned this the hard way. {idea_title}.\n1) Do this\n2) Skip that\n3) Try this\nCTA: Agree or disagree?"
    return {"A":{"text":A,"hashtags":["#learning","#careers","#productivity"]},
            "B":{"text":B,"hashtags":["#growth","#tips","#leadership"]}}

def infer_voice(profile_text: str) -> Voice:
    if not OPENAI_KEY:
        return _offline_voice(profile_text)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_KEY)
        prompt = open(os.path.join(os.path.dirname(__file__), "..","prompts","voice_prompt.txt")).read()
        messages=[{"role":"user","content":prompt + "\n\nPROFILE:\n" + profile_text}]
        resp = client.chat.completions.create(model=MODEL, messages=messages, temperature=0.2)
        content = resp.choices[0].message.content
        data = json.loads(content)
        return Voice(voice=data.get("voice",{}), pillars=data.get("pillars",[]), pitch=data.get("pitch",""))
    except Exception:
        return _offline_voice(profile_text)

def generate_ideas(industry: str, persona: str) -> list[dict]:
    if not OPENAI_KEY:
        return _offline_ideas()
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_KEY)
        prompt = open(os.path.join(os.path.dirname(__file__), "..","prompts","ideas_prompt.txt")).read()
        user = f"Industry: {industry}\nPersona: {persona}\n" + prompt
        resp = client.chat.completions.create(model=MODEL, messages=[{"role":"user","content":user}], temperature=0.5)
        content = resp.choices[0].message.content
        return json.loads(content)
    except Exception:
        return _offline_ideas()

def compose_post(idea_title: str, voice_json: dict) -> dict:
    if not OPENAI_KEY:
        return _offline_posts(idea_title)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_KEY)
        prompt = open(os.path.join(os.path.dirname(__file__), "..","prompts","post_prompt.txt")).read()
        user = f"VOICE JSON:\n{json.dumps(voice_json)}\nIDEA:\n{idea_title}\n\n{prompt}"
        resp = client.chat.completions.create(model=MODEL, messages=[{"role":"user","content":user}], temperature=0.7)
        content = resp.choices[0].message.content
        return json.loads(content)
    except Exception:
        return _offline_posts(idea_title)
