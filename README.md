# 📚 LibreLedger: Library Lending API

A REST API for running a lending library, built with **FastAPI**, **PostgreSQL**, **SQLAlchemy 2.0** and **Alembic**. It tracks books, physical copies, members, loans, late fees and payments, and it leans on the database itself to keep that data correct.

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00)
![License](https://img.shields.io/badge/License-MIT-green)

> 🚧 **Work in progress.** The database layer is finished and the API is being built phase by phase. See the [roadmap](#-roadmap) for what is done and what is next.

<!-- 
> 🖼️ **PLACEHOLDER: add a hero image here.**
> Take a screenshot of the Swagger UI at `http://127.0.0.1:8000/docs` (or a short GIF of one request) and save it as `docs/images/swagger-overview.png`.
> Then replace this block with: `![Swagger UI](docs/images/swagger-overview.png)`
-->
---

## 📖 Table of contents

- [Why this project](#-why-this-project)
- [Features](#-features)
- [Tech stack](#-tech-stack)
- [Architecture](#-architecture)
- [Database design](#-database-design)
- [Getting started](#-getting-started)
- [API overview](#-api-overview)
- [Project structure](#-project-structure)
- [Roadmap](#-roadmap)
- [What I learned](#-what-i-learned)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Why this project

I built this to move from tutorial-style CRUD with mock data to a **production-style backend**: a real relational database, versioned migrations, a layered code structure, and business rules that stay correct under pressure.

A library is a good domain for that. It has real relationships (titles, physical copies, members, loans), real rules (one borrower per copy at a time, a loan limit, due dates, fines) and real consequences when those rules are broken.

Design decisions and the reasoning behind them are written down in [`DECISIONS.md`](DECISIONS.md).

---

## ✨ Features

**Done**
- [x] Layered project structure with environment-based settings (secrets are never committed)
- [x] Health check endpoint that verifies the database connection and returns `503` when it is down
- [x] Relational schema with 8 tables, foreign keys, CHECK constraints and indexes
- [x] Versioned database migrations with Alembic

**In progress / planned**
- [ ] CRUD endpoints (GET, POST, PUT, DELETE) for loan policies and books
- [ ] Authors, book copies and members, with relationships
- [ ] Checkout and return logic with transactions and row locking
- [ ] Late fee calculation and payments
- [ ] Search, filtering, pagination and sorting
- [ ] Consistent error handling across the API
- [ ] Automated tests against an isolated test database
- [ ] A small Streamlit demo UI

---

## 🧰 Tech stack

| Area | Technology |
|---|---|
| Language | Python 3.13 |
| Web framework | FastAPI, served by Uvicorn |
| Database | PostgreSQL (**PLACEHOLDER: add your version, e.g. 17**) |
| ORM | SQLAlchemy 2.0 (declarative models) |
| Migrations | Alembic |
| Validation and settings | Pydantic v2, pydantic-settings |
| Database driver | psycopg 3 |
| Testing *(planned)* | pytest, httpx |
| Demo UI *(planned)* | Streamlit |

---

## 🏗️ Architecture

Each layer has one job, so rules live in one place and each part can be tested on its own.

```mermaid
flowchart LR
    Client["Client<br/>Swagger UI / Streamlit"] --> R["Routers<br/>HTTP in and out"]
    R --> S["Services<br/>business rules (planned)"]
    S --> C["CRUD functions<br/>database access"]
    C --> M["SQLAlchemy models"]
    M --> DB[("PostgreSQL")]
    A["Alembic migrations"] --> DB
```

- **Routers** translate HTTP requests into function calls and return the right status codes.
- **Services** hold the lending rules, so they can run inside a single transaction.
- **CRUD functions** are the only place that talks to the database.
- **Models** describe the tables, and **Alembic** keeps the real database in step with them.

---

## 🗄️ Database design

![ER diagram](docs/Database_Design.png)

<!-- > 🖼️ **PLACEHOLDER:** export your finished ER diagram as `docs/er-diagram.png`. The interactive version below renders directly on GitHub, so the image is only a fallback and can be removed if you prefer. -->

```mermaid
erDiagram
    authors {
        SERIAL id PK "Auto-increment author id"
        VARCHAR name "Author full name, 255, NOT NULL"
    }

    loan_policies {
        SERIAL policy_id PK "Auto-increment policy id"
        VARCHAR policy_name "Policy title, 100, NOT NULL"
        INTEGER loan_duration_days "CHECK greater than 0"
        INTEGER reprieve_duration_days "CHECK 0 or more"
        NUMERIC daily_penalty_rate "10,2, CHECK 0 or more"
    }

    books {
        VARCHAR isbn PK "Catalog identifier, 20"
        VARCHAR name "Book title, 255, NOT NULL"
        INTEGER edition "CHECK greater than 0"
        INTEGER policy_id FK "NOT NULL, references loan_policies"
    }

    book_authors {
        VARCHAR isbn PK, FK "References books, ON DELETE CASCADE"
        INTEGER author_id PK, FK "References authors, ON DELETE CASCADE"
    }

    book_copies {
        VARCHAR barcode PK "Physical tag, 50"
        VARCHAR isbn FK "NOT NULL, references books, RESTRICT"
    }

    members {
        VARCHAR unique_id PK "Library card token, 50"
        VARCHAR name "Member full name, 255, NOT NULL"
        INTEGER current_loans_count "Default 0, CHECK 0 to 3"
        BOOLEAN is_eligible_to_borrow "Default TRUE"
        NUMERIC total_penalty_balance "10,2, default 0.00, CHECK 0 or more"
    }

    loans {
        SERIAL loan_id PK "Auto-increment loan id"
        VARCHAR member_id FK "NOT NULL, references members, RESTRICT"
        VARCHAR barcode FK "NOT NULL, RESTRICT, partial unique index where returned_at is NULL"
        TIMESTAMPTZ borrowed_at "NOT NULL, default now"
        TIMESTAMPTZ due_at "NOT NULL, computed deadline"
        TIMESTAMPTZ reprieve_ends_at "NOT NULL, final mercy date"
        TIMESTAMPTZ returned_at "NULL while out, CHECK after borrowed_at"
        NUMERIC accumulated_penalty "10,2, default 0.00, CHECK 0 or more"
    }

    payments {
        SERIAL payment_id PK "Auto-increment payment id"
        VARCHAR member_id FK "NOT NULL, references members, RESTRICT"
        NUMERIC amount_paid "10,2, CHECK greater than 0"
        TIMESTAMPTZ paid_at "NOT NULL, default now"
    }

    authors ||--o{ book_authors : "writes CASCADE"
    books ||--o{ book_authors : "credits CASCADE"
    loan_policies ||--o{ books : "governs"
    books ||--o{ book_copies : "has copies RESTRICT"
    book_copies ||--o{ loans : "lent in RESTRICT"
    members ||--o{ loans : "borrows RESTRICT"
    members ||--o{ payments : "makes RESTRICT"
```

### The eight tables

| Table | Purpose |
|---|---|
| `loan_policies` | Loan length, grace period and daily late fee, defined once and reused |
| `books` | The catalog entry (the *title*), identified by ISBN, and the policy it follows |
| `authors` and `book_authors` | Authors, and the many-to-many link between authors and books |
| `book_copies` | Each *physical* copy of a title, identified by its barcode |
| `members` | Library members, their loan count, eligibility and fee balance |
| `loans` | The full lending history. Rows are never deleted |
| `payments` | Payments members make against their fees |

### Design highlights

- **Titles and copies are separate.** A `books` row is the idea of a book, and `book_copies` rows are the physical items on the shelf. That is how real libraries track stock, and availability is derived from loans, not stored in a flag that can drift out of sync.
- **A copy can never be lent twice.** A *partial unique index* on `loans(barcode)`, applied only where `returned_at IS NULL`, lets PostgreSQL itself reject a second active loan for the same copy, even under concurrent requests.
- **Rules live in the database too.** CHECK constraints keep counts, money and dates sane (no negative fees, no return before checkout, due dates in order).
- **History is never deleted.** Returned loans stay in the table, so fines and payments can always be traced back to what happened.
- **Safe money and time.** Money is `NUMERIC(10,2)`, never a float, and every timestamp is timezone-aware.
- **Foreign keys are protected and indexed.** Deleting a record that others depend on is refused, and the foreign key columns are indexed for fast joins.
- **Predictable names.** A naming convention gives every constraint and index a stable name, which keeps migrations reliable.

---

## 🚀 Getting started

### Prerequisites

- Python 3.11 or newer (developed on 3.13)
- PostgreSQL installed and running locally
- Git

### 1. Clone and install

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME

python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Create the database

Open `psql` (or pgAdmin's Query Tool) and run:

```sql
CREATE USER bookshelf_user WITH PASSWORD 'choose-a-strong-password';
CREATE DATABASE bookshelf_db OWNER bookshelf_user;
```

### 3. Configure the environment

Copy the example file and fill in your own values:

```bash
cp .env.example .env        # Windows: copy .env.example .env
```

```env
DATABASE_URL=postgresql+psycopg://bookshelf_user:YOUR_PASSWORD@localhost:5432/bookshelf_db
```

> The URL must include the driver name (`postgresql+psycopg://`). If your password contains special characters such as `@` or `#`, URL-encode them. `.env` is git-ignored and must never be committed.

### 4. Create the tables

```bash
alembic upgrade head
```

### 5. Run the API

```bash
uvicorn app.main:app --reload
```

- Interactive docs: <http://127.0.0.1:8000/docs>
- Health check: <http://127.0.0.1:8000/health>

---

## 🔌 API overview

**Available now**

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Confirms the app is up and the database is reachable (`503` if not) |

**Planned** *(paths may change as the API takes shape)*

| Resource | Methods | Phase |
|---|---|---|
| Loan policies | GET, POST, PUT, DELETE | 2 |
| Books | GET, POST, PUT, DELETE | 2 |
| Authors, copies, members | GET, POST, PUT, DELETE | 3 |
| Loans (checkout and return) | GET, POST | 4 |
| Payments | GET, POST | 4 |

<!-- > 🖼️ **PLACEHOLDER:** once endpoints exist, add a screenshot of the Swagger UI endpoint list here (`docs/images/endpoints.png`). -->

---

## 📁 Project structure

```
.
├── app/
│   ├── main.py            # creates the app and registers routers
│   ├── core/              # settings and configuration
│   ├── db/                # engine, sessions, model registry
│   ├── models/            # SQLAlchemy table definitions
│   ├── routers/           # HTTP layer
│   ├── schemas/           # Pydantic request/response models (planned)
│   ├── crud/              # database access functions (planned)
│   └── services/          # business rules (planned)
├── migrations/            # Alembic migration history
├── docs/                  # ER diagram, setup notes, images
├── tests/                 # test suite (planned)
├── DECISIONS.md           # design decisions and why
├── .env.example           # template for local settings
└── requirements.txt
```

---

## 🗺️ Roadmap

- [x] **Phase 0:** project skeleton, settings, health check
- [x] **Phase 1:** schema design, SQLAlchemy models, Alembic migrations
- [ ] **Phase 2:** database sessions, loan policies and books CRUD
- [ ] **Phase 3:** authors, copies, members, relationships, query efficiency
- [ ] **Phase 4:** checkout and return rules, transactions, locking, fees and payments
- [ ] **Phase 5:** search, pagination, error handling, Streamlit demo UI
- [ ] **Phase 6:** automated tests, documentation, polish

---

<!-- ## 💡 What I learned

> ✏️ **PLACEHOLDER: rewrite these in your own words.** They are starting points based on real moments from the build, and a short, honest section like this is memorable to readers.

- **Constraints belong in the database.** A rule in Python can be bypassed. A rule in PostgreSQL applies to every writer.
- **Migrations are transactional.** A failed migration rolled back completely, so a typo cost nothing and left no half-built tables.
- **SQL inside strings is not spell-checked.** A column name misspelled in a CHECK constraint only fails when the migration runs, so read generated migrations before applying them.
- **A flag column can drift, so derive state when you can.** Replacing an `is_available` flag with a partial unique index removed a whole class of bugs. -->

---

## 📄 License

Released under the [MIT License](LICENSE).

---

<!-- ## 📬 Contact

> ✏️ **PLACEHOLDER:** add your details.

**Your Name**: [LinkedIn](https://www.linkedin.com/in/YOUR-PROFILE) · [GitHub](https://github.com/YOUR-USERNAME) · your.email@example.com -->
