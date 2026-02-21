from datetime import datetime
from app.database import get_session
from app.models import Application

def test_log_insert():
    with get_session() as s:
        a = Application(datetime_utc=datetime.utcnow(), company="TestCo", title="TestTitle", status="parsed")
        s.add(a); s.commit(); s.refresh(a)
        assert a.id is not None
