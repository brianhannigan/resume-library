from __future__ import annotations
from sqlmodel import SQLModel, Session, create_engine

engine = create_engine("sqlite:///autoapply.sqlite", echo=False)

def get_session():
    return Session(engine)
