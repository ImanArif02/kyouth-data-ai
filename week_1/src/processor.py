from pathlib import Path
from bs4 import BeautifulSoup
from pydantic import BaseModel
import json


class JobListing(BaseModel):
    source_id: str
    job_title: str
    company: str
    description: str

def process_all_html(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    processed = 0
    skipped = 0

    print("🥈 Silver:")

    for file in input_dir.glob("*.html"):
        total += 1

        try:
            html_content = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            soup = BeautifulSoup(
                html_content,
                "html.parser"
            )

            # source_id
            url_meta = soup.find(
                "meta",
                property="og:url"
            )

            if not url_meta:
                print(f"⚠ Missing source_id in: {file.name}")
                skipped += 1
                continue

            url = url_meta["content"]

            source_id = url.split("/")[-1]

            print(source_id)

            #job_title
            title_tag = soup.find(
                attrs={"data-automation": "job-detail-title"}
            )

            if not title_tag:
                print(f"⚠ Missing job_title in: {file.name}")
                skipped += 1
                continue

            job_title = title_tag.get_text(
                separator=" ",
                strip=True
            )

            description_tag = soup.find(
                 attrs={"data-automation": "jobAdDetails"}
            )

            if not description_tag:
                print(f"⚠ Missing description in: {file.name}")
                skipped += 1
                continue

            description = description_tag.get_text(
                separator=" ",
                strip=True
            )

            print(description[:100])

            #company
            company_tag = soup.find(
                attrs={"data-automation": "advertiser-name"}
            )

            if not company_tag:
                print(f"⚠ Missing company in: {file.name}")
                skipped += 1
                continue

            company = company_tag.get_text(
                separator=" ",
                strip=True
            )

            print(f"Company Length: {len(company)}")

            if not source_id.strip():
                print(f"⚠ Missing source_id in: {file.name}")
                skipped += 1
                continue

            if not job_title.strip():
                print(f"⚠ Missing job_title in: {file.name}")
                skipped += 1
                continue

            if not company.strip():
                print(f"⚠ Missing company in: {file.name}")
                skipped += 1
                continue

            if not description.strip() or len(description.strip()) < 30:
                print(f"⚠ Missing description in: {file.name}")
                skipped += 1
                continue

            print(company)

            job = JobListing(
                source_id=source_id,
                job_title=job_title,
                company=company,
                description=description
            )

            print(job_title)
            
            output_file = output_dir / f"{source_id}.json"

            output_file.write_text(
                job.model_dump_json(indent=4),
                encoding="utf-8"
            )

            print(f"✅ Processed: {file.name}")

            processed += 1

            print("Reading:", file.name)

        except Exception as e:
            print(f"❌ Error in {file.name}")
            print(e)
            skipped += 1

    print("\n📊 Silver Summary:")
    print(f"Total: {total} | Processed: {processed} | Skipped: {skipped}")