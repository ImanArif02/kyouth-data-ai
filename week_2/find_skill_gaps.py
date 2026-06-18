from pydantic import BaseModel
import sqlite3


class SkillGapResult(BaseModel):
    gaps: list[str]

def normalize_skill(skill: str) -> str:
    skill = skill.strip().lower()

    replacements = {
        "powerbi": "power bi",
        "ms sql": "sql server",
        "postgres": "postgresql",
        "rest apis": "rest api",
    }

    return replacements.get(skill, skill)

def extract_resume_skills(resume_text: str) -> set[str]:
    skills = set()

    for line in resume_text.splitlines():
        if line.lower().startswith("technical skills:"):
            skill_text = line.split(":", 1)[1]

            for skill in skill_text.split(","):
                skill = normalize_skill(skill)

                if "/" in skill and skill not in ["ci/cd", "a/b testing"]:
                    for sub_skill in skill.split("/"):
                        skills.add(normalize_skill(sub_skill))
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
        for skill in tech_stack.split(","):
            clean_skill = normalize_skill(skill)

            if clean_skill == "no tech stack extracted":
                continue

            if "/" in clean_skill and clean_skill not in ["ci/cd", "a/b testing"]:
                for sub_skill in clean_skill.split("/"):
                    sub_skill = normalize_skill(sub_skill)
                    if sub_skill:
                        skills.add(sub_skill)
            elif clean_skill:
                skills.add(clean_skill)
    return skills

def find_skill_gaps(input_file_path: str, db_url: str) -> SkillGapResult:
    try:
        with open(input_file_path, "r", encoding="utf-8") as file:
            resume_text = file.read()

        resume_skills = extract_resume_skills(resume_text)
        market_skills = extract_market_skills(db_url)
        gaps = market_skills - resume_skills

        return SkillGapResult(gaps=sorted(gaps))

    except Exception as error:
        print(f"[Skill Gap Error] {error}")
        return SkillGapResult(gaps=[])


if __name__ == "__main__":
    result = find_skill_gaps("data/resume_d3.txt", "data/jobs_d1.db")
    print(result)