from app.models.base import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class BookAuthor(Base):
    __tablename__ = "book_authors"

    isbn: Mapped[str] = mapped_column(String(20), ForeignKey(
        "books.isbn", ondelete="CASCADE",), primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        "authors.id", ondelete="CASCADE"), index=True, primary_key=True)
