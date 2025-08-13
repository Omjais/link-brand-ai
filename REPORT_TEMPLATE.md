# Technical Report (Template)

## 1. Overview
This MVP demonstrates an autonomous LinkedIn personal branding agent that researches topics, generates content, schedules posts, and tracks performance in a simplified environment.

## 2. AI Models
- Primary: OpenAI Chat Completions (configurable model, default `gpt-4o-mini`).
- Offline fallback: deterministic templates.

## 3. Pipelines
- Profile → Voice inference → Content pillars
- Industry → Ideas → A/B Post Generation
- Scheduler → Poster (simulated) → Analytics

## 4. Data
CSV-backed tables: profiles, ideas, posts, schedules, analytics.

## 5. Limitations & Future Work
- Real LinkedIn OAuth + posting
- DB migration to Postgres
- Fine-tuned hashtag analytics
- Real A/B testing over time
