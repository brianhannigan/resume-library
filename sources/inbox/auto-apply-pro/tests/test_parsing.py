from app.jd_parser import parse_from_text

def test_parse_text():
    txt = "This is a job. Responsibilities include A, B, C."
    out = parse_from_text(txt)
    assert "Responsibilities" in out
