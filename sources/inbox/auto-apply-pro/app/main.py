from __future__ import annotations
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from .database import get_session
from .models import Application
from .jd_parser import parse_from_url, parse_from_text
from .resume import load_profile_json, load_resume_txt
from .cl_generator import generate_cover_letter, write_outputs
from .config import CFG, DEFAULT_PROFILE

app = FastAPI(title="Auto-Apply Pro")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/applications", response_class=HTMLResponse)
def applications(request: Request, q: str | None = None):
    with get_session() as s:
        if q:
            rows = s.exec(
                f"SELECT * FROM applications WHERE company LIKE '%{q}%' OR title LIKE '%{q}%' ORDER BY datetime_utc DESC"
            ).all()
        else:
            rows = s.exec("SELECT * FROM applications ORDER BY datetime_utc DESC").all()
    return templates.TemplateResponse("applications.html", {"request": request, "rows": rows})

@app.get("/applications/{app_id}", response_class=HTMLResponse)
def application_detail(request: Request, app_id: int):
    with get_session() as s:
        row = s.get(Application, app_id)
    return templates.TemplateResponse("application_detail.html", {"request": request, "row": row})

@app.get("/upload", response_class=HTMLResponse)
def upload_form(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
def generate(request: Request,
             url: str = Form(None),
             text: str = Form(None),
             profile: str = Form(DEFAULT_PROFILE),
             tone: str = Form("confident")):
    jd = parse_from_url(url) if url else parse_from_text(text or "")
    profile_data = load_profile_json(profile)
    cl = generate_cover_letter(jd, profile_data, tone=tone, template_name=CFG["defaults"].get("template","default"))
    company = profile_data.get("target_company","(Unknown Company)")
    title = profile_data.get("target_title","(Unknown Title)")
    out = write_outputs(cl, f"{company}_{title}".replace(" ", "_"), CFG["paths"]["cover_letter_dir"])
    with get_session() as s:
        app_row = Application(
            datetime_utc=datetime.utcnow(),
            company=company,
            title=title,
            source="web",
            location=profile_data.get("location"),
            job_url=url,
            status="generated",
            profile_used=profile,
            resume_path=CFG["paths"]["resume_pdf"],
            cover_letter_path=out["txt"],
        )
        s.add(app_row); s.commit(); s.refresh(app_row)
    return templates.TemplateResponse("cover_letter.html", {"request": request, "cl": cl, "out": out, "app_id": app_row.id})
