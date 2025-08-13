# SkillBank — Time-based Skill Swap

Trade skills with time credits. 1 hour = 1 credit. No money.

## Features
- Auth, profiles, reputation
- Offers/Requests directory with HTMX filters
- Matching flow: propose → accept → done
- Ledger wallet with balance and history
- Reviews and reputation updates
- Tailwind UI, WhiteNoise static, simple service worker

## Tech Stack
- Django 5.x, HTMX, Django Templates
- Tailwind (CDN for MVP), Crispy-Forms + Tailwind
- SQLite (can mount to /data in prod), WhiteNoise
- pytest + pytest-django

## Local Setup
```bash
# macOS / Linux
cd skillbank
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt || pip install -e .  # if using pyproject only
python manage.py migrate
python manage.py createsuperuser
# optional: seed demo
python manage.py shell -c "from scripts.seed_data import run; run()"
python manage.py runserver
```

Visit: `/offers/`, `/requests/`, `/matches/`, `/wallet/`, `/reviews/pending`.

Demo login: user1@example.com / demodemo (after seeding).

## Environment
- `DATABASE_URL` (optional) e.g. `sqlite:////data/db.sqlite3`
- `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`
- `SECRET_KEY` (set in production)

## Deployment (Render/Fly/Railway)
1. Create app, attach a small persistent volume mounted at `/data`
2. Set env:
   - `DATABASE_URL=sqlite:////data/db.sqlite3`
   - `DEBUG=0`, `ALLOWED_HOSTS=your-domain`
3. Build & run steps:
   - Install deps: `pip install -r requirements.txt`
   - `python manage.py collectstatic --noinput`
   - `python manage.py migrate`
   - `gunicorn core.wsgi:application --bind 0.0.0.0:$PORT`

Static files are served via WhiteNoise; `/static/service-worker.js` is registered.

## Testing
```bash
pytest -q
```

## Architecture
- Apps: `accounts/`, `directory/`, `matches/`, `ledger/`, `reviews/`
- Templates in `templates/` with reusable partials for HTMX swaps
- Ledger is immutable; balance computed as incoming − outgoing

## Security & Privacy
- CSRF protected (forms, HTMX header injection)
- Basic permissions on match actions and CRUD ownership
- SQLite file on a volume; no third-party APIs or AI

## License
MIT

## Roadmap
- Full Tailwind build pipeline (PostCSS)
- Rich notifications and email (optional)
- More robust rate limiting and moderation

