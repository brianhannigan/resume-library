from app.cl_generator import generate_cover_letter
from app.resume import load_profile_json

def test_generate_rules():
    prof = load_profile_json("software-engineer")
    cl = generate_cover_letter("We need someone skilled in Python and C#", prof, "confident")
    assert "Dear" in cl or "Hello" in cl
    assert "Software Engineer" in cl or prof.get("target_title","") in cl
