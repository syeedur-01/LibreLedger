from app.models.base import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class BookCopy (Base):

    __tablename__ = "book_copies"

    barcode: Mapped[str] = mapped_column(String(50), primary_key=True)
    isbn: Mapped[str] = mapped_column(String(20), ForeignKey(
        "books.isbn", ondelete="RESTRICT"), index=True, nullable=False)
