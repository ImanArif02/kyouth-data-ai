import re
import sqlite3
from pathlib import Path

from pydantic import BaseModel


class SkillGapResult(BaseModel):
    gaps: list[str]


SKILL_ALIASES = {
    "powerbi": "power bi",
    "power bi": "power bi",
    "ms sql": "sql server",
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "rest apis": "rest api",
    "restful api design and development": "rest api",
    "api integration or web automation": "api",
    "aws deployment and maintenance": "aws",
    "linux development environments": "linux",
}


def normalize_skill(skill: str) -> str:
    skill = skill.strip().lower()
    skill = re.sub(r"\s+", " ", skill)
    return SKILL_ALIASES.get(skill, skill)


def split_skill_text(skill_text: str) -> set[str]:
    skills = set()

    for skill in re.split(r",|\n|•|-", skill_text):
        skill = normalize_skill(skill)

        if not skill:
            continue

        if "/" in skill and skill not in {"ci/cd", "a/b testing"}:
            for sub_skill in skill.split("/"):
                sub_skill = normalize_skill(sub_skill)
                if sub_skill:
                    skills.add(sub_skill)
        else:
            skills.add(skill)

    return skills


def extract_market_skills(db_url: str) -> set[str]:
    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tech_stack
        FROM jobs
        WHERE tech_stack IS NOT NULL
    """)

    rows = cursor.fetchall()
    conn.close()

    skills = set()

    for (tech_stack,) in rows:
        for skill in split_skill_text(tech_stack):
            if skill != "no tech stack extracted":
                skills.add(skill)

    return skills


def extract_resume_skills(resume_text: str, market_skills: set[str]) -> set[str]:
    resume_text = resume_text.lower()
    found_skills = set()

    for skill in market_skills:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, resume_text):
            found_skills.add(skill)

    return found_skills


def find_skill_gaps_from_text(resume_text: str, db_url: str) -> SkillGapResult:
    try:
        market_skills = extract_market_skills(db_url)
        resume_skills = extract_resume_skills(resume_text, market_skills)
        gaps = market_skills - resume_skills

        return SkillGapResult(gaps=sorted(gaps))

    except sqlite3.Error as error:
        print(f"[Skill Gap Error] {error}")
        return SkillGapResult(gaps=[])

    except Exception as error:
        print(f"[Unexpected Error] {error}")
        return SkillGapResult(gaps=[])

def find_skill_gaps(input_file_path: str, db_url: str) -> SkillGapResult:
    try:
        resume_text = Path(input_file_path).read_text(encoding="utf-8")

        market_skills = extract_market_skills(db_url)
        resume_skills = extract_resume_skills(resume_text, market_skills)
        gaps = market_skills - resume_skills

        return SkillGapResult(gaps=sorted(gaps))

    except (OSError, sqlite3.Error) as error:
        print(f"[Skill Gap Error] {error}")
        return SkillGapResult(gaps=[])

    except Exception as error:
        print(f"[Unexpected Error] {error}")
        return SkillGapResult(gaps=[])


if __name__ == "__main__":
    result = find_skill_gaps("data/resume_d3.txt", "data/jobs_d1.db")
    print(result)
