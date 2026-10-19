from decimal import Decimal
from app.models.base import Base
from sqlalchemy import String, Integer, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column


class LoanPolicy (Base):
    __tablename__ = "loan_policies"

    policy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    policy_name: Mapped[str] = mapped_column(String(100), nullable=False)
    loan_duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    reprieve_duration_days: Mapped[int] = mapped_column(
        Integer, nullable=False)
    daily_penalty_rate: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint("loan_duration_days>0", name="duration_pos"),
        CheckConstraint("reprieve_duration_days>0", name="reprieve_pos"),
        CheckConstraint("daily_penalty_rate >= 0.00", name="rate_pos"),

    )
