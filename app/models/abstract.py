from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, CheckConstraint

from app.core.db import Base
from app.utils.constans import DEFAULT_INVESTED_AMOUNT


class Abstract(Base):

    __abstract__ = True

    __table_args__ = (
        CheckConstraint('invested_amount >= 0', name='check_invested_amount_positive'),
        CheckConstraint('invested_amount <= full_amount', name='check_invested_amount_not_exceed_full')
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=DEFAULT_INVESTED_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
