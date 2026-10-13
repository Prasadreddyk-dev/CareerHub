"""
backend/ai/skills.py
Deterministic skill cleaning and matching. No AI, no database.
"""
import re

# lowercase variant -> canonical display name. Extend as you see real job posts.
CANONICAL = {
    "python": "Python",
    "py": "Python",
    "django": "Django",
    "drf": "Django REST Framework",
    "django rest": "Django REST Framework",
    "django rest framework": "Django REST Framework",
    "postgres": "PostgreSQL",
    "postgre sql": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "psql": "PostgreSQL",
    "sql": "SQL",
    "rest api": "REST APIs",
    "rest apis": "REST APIs",
    "rest api development": "REST APIs",
    "restful api": "REST APIs",
    "restful apis": "REST APIs",
    "git": "Git",
    "github": "GitHub",
    "docker": "Docker",
    "redis": "Redis",
    "aws": "AWS",
    "amazon web services": "AWS",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
}


def clean(skill) -> str:
    """Trim, collapse spaces, drop '(notes)' and trailing punctuation."""
    if not isinstance(skill, str):
        return ""
    text = re.sub(r"\(.*?\)", "", skill)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" .,;:")


def canonical_name(skill) -> str:
    cleaned = clean(skill)
    return CANONICAL.get(cleaned.lower(), cleaned)


def normalize_many(skills) -> list[str]:
    """Clean, map to canonical names, remove duplicates, keep order."""
    seen: dict[str, str] = {}
    for raw in skills:
        name = canonical_name(raw)
        if name:
            seen.setdefault(name.lower(), name)
    return list(seen.values())


def compare_skills(required, user_skills) -> dict:
    required = normalize_many(required)
    user_keys = {name.lower() for name in normalize_many(user_skills)}

    matched = [s for s in required if s.lower() in user_keys]
    missing = [s for s in required if s.lower() not in user_keys]
    percentage = round(100 * len(matched) / len(required), 2) if required else 0

    return {"matched": matched, "missing": missing, "percentage": percentage}