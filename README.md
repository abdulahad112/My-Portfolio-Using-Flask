# Flask Portfolio - Ready to run

This is a minimal, ready-to-run Flask portfolio project created for you.

## Quick start

1. Create and activate a virtualenv

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. (Optional) Edit `.env_example` and rename to `.env` with your secrets.

3. Initialize the database (optional, for storing contact messages):

```bash
export FLASK_APP=app.py
flask db init
flask db migrate -m "init"
flask db upgrade
```

4. Run the app:

```bash
python app.py
```

Open http://127.0.0.1:5000/ in your browser.
