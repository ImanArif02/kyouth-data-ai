import logging

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
                logging.warning(f"Missing source_id in: {file.name}")
                skipped += 1
                continue

            url = url_meta["content"]

            source_id = url.split("/")[-1]

            #job_title
            title_tag = soup.find(
                attrs={"data-automation": "job-detail-title"}
            )

            if not title_tag:
                logging.warning(f"Missing job_title in: {file.name}")
                skipped += 1
                continue

            job_title = title_tag.get_text(
                separator=" ",
                strip=True
            )
            
            #description 
            description_tag = soup.find(
                 attrs={"data-automation": "jobAdDetails"}
            )

            if not description_tag:
                logging.warning(f"Missing description in: {file.name}")
                skipped += 1
                continue

            description = description_tag.get_text(
                separator=" ",
                strip=True
            )

            #company
            company_tag = soup.find(
                attrs={"data-automation": "advertiser-name"}
            )

            if not company_tag:
                logging.warning(f"Missing company in: {file.name}")
                skipped += 1
                continue

            company = company_tag.get_text(
                separator=" ",
                strip=True
            )

            if not source_id.strip():
                logging.warning(f"Missing source_id in: {file.name}")
                skipped += 1
                continue

            if not job_title.strip():
                logging.warning(f"Missing job_title in: {file.name}")
                skipped += 1
                continue

            if not company.strip():
                logging.warning(f"Missing company in: {file.name}")
                skipped += 1
                continue

            if not description.strip() or len(description.strip()) < 30:
                logging.warning(f"Missing description in: {file.name}")
                skipped += 1
                continue

            job = JobListing(
                source_id=source_id,
                job_title=job_title,
                company=company,
                description=description
            )
         
            output_file = output_dir / f"{source_id}.json"

            output_file.write_text(
                job.model_dump_json(indent=4),
                encoding="utf-8"
            )

            logging.info(f"✅ Processed: {file.name}")

            processed += 1

        except Exception as e:
            logging.error(
                f"Failed processing {file.name}: {e}"
            )
            skipped += 1

    print("\n📊 Silver Summary:")
    print(f"Total: {total} | Processed: {processed} | Skipped: {skipped}")