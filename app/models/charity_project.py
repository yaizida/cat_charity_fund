from sqlalchemy import Column, String, Text

from .abstract import Abstract
from app.utils.constans import MAX_LEN_STRING


class CharityProject(Abstract):
    name = Column(String(MAX_LEN_STRING), unique=True, nullable=False)
    description = Column(Text, nullable=False)
