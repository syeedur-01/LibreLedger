from sqlalchemy import Integer, String, ForeignKey, CheckConstraint
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Book(Base):

    __tablename__ = "books"

    isbn: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    edition: Mapped[int] = mapped_column(Integer, nullable=False)
    policy_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        "loan_policies.policy_id", ondelete="RESTRICT"), index=True, nullable=False)

    __table_args__ = (
        CheckConstraint("edition > 0", name="edition_pos"),
    )
