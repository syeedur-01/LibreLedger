# Bookshelf

A minimal FastAPI application scaffold.

See [docs/setup.md](docs/setup.md) for setup and run instructions.
bookshelf/
├── app/
│   ├── __init__.py
│   ├── main.py                  # creates the app, registers routers
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # settings loaded from .env
│   │   └── exceptions.py        # custom errors + handlers (Phase 5)
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py              # declarative base, imports all models
│   │   └── session.py           # engine + per-request session dependency
│   ├── models/                  # database tables
│   │   ├── __init__.py
│   │   ├── author.py
│   │   ├── book.py              # includes the book-author link table
│   │   ├── member.py
│   │   └── loan.py
│   ├── schemas/                 # Pydantic request/response shapes
│   │   ├── __init__.py
│   │   ├── author.py
│   │   ├── book.py
│   │   ├── member.py
│   │   └── loan.py
│   ├── crud/                    # functions that talk to the database
│   │   ├── __init__.py
│   │   ├── author.py
│   │   ├── book.py
│   │   ├── member.py
│   │   └── loan.py
│   ├── services/                # business rules (Phase 4)
│   │   ├── __init__.py
│   │   └── loan_service.py
│   └── routers/                 # thin HTTP layer
│       ├── __init__.py
│       ├── health.py
│       ├── authors.py
│       ├── books.py
│       ├── members.py
│       └── loans.py
├── frontend/
│   └── streamlit_app.py         # separate demo UI (Phase 5)
├── migrations/                  # Alembic
│   ├── versions/
│   └── env.py
├── tests/
│   ├── conftest.py              # test database + client setup
│   ├── test_books.py
│   ├── test_authors.py
│   ├── test_members.py
│   └── test_loans.py
├── docs/
│   └── setup.md                 # local PostgreSQL setup steps
├── .env                         # real credentials, never committed
├── .env.example                 # safe template, committed
├── .gitignore
├── alembic.ini
├── requirements.txt
├── DECISIONS.md
└── README.md