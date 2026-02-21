from __future__ import annotations
import csv
from datetime import datetime
from pathlib import Path
import typer
from app.jd_parser import parse_from_url, parse_from_text
from app.resume import load_profile_json
from app.cl_generator import generate_cover_letter, write_outputs
from app.automation.apply_flow import apply_once, log_result
from app.database import get_session
from app.models import Application
from app.config import CFG, DEFAULT_PROFILE

app = typer.Typer(add_completion=False, help="Auto-Apply Pro CLI")

@app.command()
def parse(url: str = typer.Option(None, help="Job URL"),
          text: str = typer.Option(None, help="Job description text")):
    jd = parse_from_url(url) if url else parse_from_text(text or "")
    typer.echo(jd[:1000] + ("..." if len(jd) > 1000 else ""))

@app.command("generate-cl")
def generate_cl(url: str = typer.Option(None),
                text: str = typer.Option(None),
                profile: str = typer.Option(DEFAULT_PROFILE),
                tone: str = typer.Option("confident")):
    jd = parse_from_url(url) if url else parse_from_text(text or "")
    prof = load_profile_json(profile)
    cl = generate_cover_letter(jd, prof, tone, CFG["defaults"].get("template","default"))
    company = prof.get("target_company","Acme")
    title = prof.get("target_title","Software Engineer")
    out = write_outputs(cl, f"{company}_{title}".replace(" ","_"), CFG["paths"]["cover_letter_dir"])
    typer.echo(f"Saved: {out}")

@app.command()
def apply(url: str,
          confirm: bool = typer.Option(True),
          dry_run: bool = typer.Option(False),
          profile: str = typer.Option(DEFAULT_PROFILE),
          tone: str = typer.Option("confident")):
    prof = load_profile_json(profile)
    ctx = {
        "first_name": prof.get("first_name",""),
        "last_name": prof.get("last_name",""),
        "contact_email": prof.get("contact_email",""),
        "contact_phone": prof.get("contact_phone",""),
        "location": prof.get("location",""),
        "linkedin_url": prof.get("linkedin_url",""),
        "github_url": prof.get("github_url",""),
        "resume_pdf": CFG["paths"]["resume_pdf"],
        "cover_letter_text": prof.get("cover_letter_fallback",""),
        "company": prof.get("target_company",""),
        "title": prof.get("target_title",""),
        "profile_used": profile,
    }
    result = apply_once(url, ctx, confirm=confirm, dry_run=dry_run)
    app_id = log_result(url, result, ctx)
    typer.echo(f"Application logged: #{app_id} -> {result}")

@app.command()
def import_(csv_path: str,
            dry_run: bool = typer.Option(True)):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            typer.echo(f"Queued: {row['company']} - {row['title']} ({row['url']}) dry_run={dry_run}")

@app.command("log")
def export_log(export: str,
               since: str = typer.Option("1970-01-01")):
    Path(export).parent.mkdir(parents=True, exist_ok=True)
    with get_session() as s:
        rows = s.exec("SELECT * FROM applications WHERE datetime_utc >= :since",
                      params={"since": since}).all()
    import pandas as pd
    df = pd.DataFrame([r.model_dump() for r in rows])
    df.to_csv(export, index=False)
    typer.echo(f"Exported {len(df)} rows to {export}")

def main():
    app()

if __name__ == "__main__":
    main()
