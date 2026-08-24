# Windows quick setup

```cmd
cd cognodb_movie_explorer
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
notepad .env
python scripts\seed.py
python -m app.main
```

Open http://127.0.0.1:5000
