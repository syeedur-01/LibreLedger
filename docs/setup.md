# Setup

## Install dependencies

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configure environment

Copy `.env.example` to `.env` and adjust the values as needed.

## Run the application

```powershell
uvicorn app.main:app --reload
```
