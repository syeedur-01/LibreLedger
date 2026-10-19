from decimal import Decimal
from app.models.base import Base
from sqlalchemy import Integer, String, Boolean, CheckConstraint, Numeric, text
from sqlalchemy.orm import Mapped, mapped_column


class Member (Base):
    __tablename__ = "members"

    unique_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    current_loans_count: Mapped[int] = mapped_column(
        Integer, server_default=text("0"), nullable=False)
    is_eligible_to_borrow: Mapped[bool] = mapped_column(
        Boolean, server_default=text("true"), nullable=False)
    total_penalty_balance: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), server_default=text("0.00"), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "current_loans_count >= 0 AND current_loans_count <= 3",
            name="loans_count_bounds"
        ),
        CheckConstraint(
            "total_penalty_balance >= 0.00",
            name="balance_nonneg"
        ),
    )
