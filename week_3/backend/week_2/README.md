
# Week 2: AI Component - Resume Skill Gap Analyzer

## Project Overview
This project uses Gemini AI to extract technical skills from job descriptions and store them in a SQLite database. The extracted technologies are then compared against skills found in a resume to identify skill gaps. The system combines AI-based information extraction with deterministic skill comparison to provide consistent and reproducible results.

## Setup Instructions
1. Create and activate virtual environment:
```bash
uv venv
source .venv/bin/activate
````

2. Install dependencies:

```bash
uv add google-genai python-dotenv pydantic
```

3. Create `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Do not commit `.env`.

## Usage

Run tech stack tagging:

```bash
uv run tag_data.py
```

Run skill gap analysis:

```bash
uv run find_skill_gaps.py
```

Run prompt model test:

```bash
uv run prompt_model.py
```

## API / Function Reference

### `prompt_model(model: str, prompt: str) -> str`

Prompts the selected Gemini model and returns a text response. It validates unsupported models and handles Gemini errors gracefully.

### `tag_data(db_url: str)`

Reads job descriptions from the SQLite `jobs` table, sends them to Gemini in batches, and updates the `tech_stack` column.

### `find_skill_gaps(input_file_path: str, db_url: str) -> SkillGapResult`

Reads resume skills and job tech stacks, normalizes them, and returns missing skills as a sorted lowercase list.

## Data / Assumptions

* Input database: `data/jobs_d1.db`
* Resume file: `data/resume_d3.txt`
* The database has a `jobs` table with `source_id`, `description`, and `tech_stack`.
* Resume skills are extracted from the `Technical Skills:` line.
* Skills are normalized to lowercase.
* Slash-separated skills such as `AWS/Azure/GCP` are split into separate skills.
* Exceptions such as `CI/CD` and `A/B testing` are kept as one skill.
* Empty Gemini results are stored as `no tech stack extracted`.

## Testing

The system was tested using the provided sample database with 8 jobs.

Commands used:

```bash
uv run tag_data.py
uv run find_skill_gaps.py
python -m py_compile tag_data.py
python -m py_compile find_skill_gaps.py
python -m py_compile prompt_model.py
```

Validation checks:

* Confirmed no syntax errors.
* Confirmed `tech_stack IS NULL` count became 0.
* Confirmed skill gaps output is lowercase and sorted.
* Confirmed deterministic output by using Python set comparison instead of LLM for Day 3-4.

## Limitations

* Gemini output may miss some job IDs, so a placeholder is used.
* The resume parser currently expects a `Technical Skills:` line.
* Skill normalization only covers selected known variants.
* The quality of Day 3-4 gaps depends on the quality of Day 1-2 tagging.
* Gemini API quota limits may affect full runs.

## Architecture Reflection

I used Gemini for Day 1-2 because job descriptions are unstructured text and LLMs are suitable for extracting technologies from natural language. For Day 3-4, I avoided using LLMs because the requirement emphasizes determinism. The skill gap logic uses normalized sets and set difference, which gives consistent results across runs.

Batching was used in `tag_data.py` to reduce API calls and better respect rate limits. Error handling and placeholders were added so the pipeline can continue even when Gemini returns empty or incomplete responses.

````

After saving, run:

```bash
python -m py_compile tag_data.py find_skill_gaps.py prompt_model.py
````
