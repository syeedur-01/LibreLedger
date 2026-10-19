from decimal import Decimal
from datetime import datetime
from app.models.base import Base
from sqlalchemy import Integer, String, CheckConstraint, Numeric, text, ForeignKey, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column


class Loan (Base):
    __tablename__ = "loans"

    loan_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id: Mapped[str] = mapped_column(String(50), ForeignKey(
        "members.unique_id", ondelete="RESTRICT"), index=True, nullable=False)
    barcode: Mapped[str] = mapped_column(String(50), ForeignKey(
        "book_copies.barcode", ondelete="RESTRICT"), index=True, nullable=False)
    borrowed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)
    due_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),  nullable=False)
    reprieve_ends_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False)
    returned_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),  nullable=True)
    accumulated_penalty: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), server_default=text("0.00"), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "returned_at IS NULL OR returned_at >= borrowed_at",
            name="return_after_borrow"
        ),
        CheckConstraint(
            "accumulated_penalty >= 0.00",
            name="penalty_nonneg"
        ),
        CheckConstraint(
            "due_at >= borrowed_at AND reprieve_ends_at >= due_at",
            name="dates_timeline_order"
        ),
        Index(
            "uq_prevent_duplicate_active_loans",
            "barcode",
            unique=True,
            postgresql_where=text("returned_at IS NULL")

        ),
    )
