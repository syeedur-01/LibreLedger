from decimal import Decimal
from datetime import datetime
from sqlalchemy import String, Integer, Numeric, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class Payment(Base):
    __tablename__ = "payments"

    # 1. Identity & Reference Fields (Strict Foreign Key String Matching)
    payment_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    member_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("members.unique_id", ondelete="RESTRICT"),
        nullable=False
    )

    # 2. Precise Financial Ledger Column
    amount_paid: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    # 3. Transaction Audit Timestamp
    paid_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # 4. Strict Named Value Validation Guardrail
    __table_args__ = (
        CheckConstraint(
            "amount_paid > 0.00",
            name="payment_amount_pos"
        ),
    )
