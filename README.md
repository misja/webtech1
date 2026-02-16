# Webtechnologie 1 - Cursusmateriaal

Onderwijsmateriaal voor de module Webtechnologie HBO-ICT jaar 1 semester 2.

## Setup voor ontwikkelaars

Deze documentatie wordt gebouwd met MkDocs. We gebruiken moderne Python tooling (`uv` + `pyproject.toml`).

### Vereisten

- Python 3.11 of hoger
- [uv](https://github.com/astral-sh/uv) - snelle Python package manager

### Installatie uv (als je het nog niet hebt)

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Of via pip
pip install uv
```

### Project setup

```bash
# Clone de repository
git clone <repo-url>
cd webtech1

# Sync dependencies met uv (super snel!)
uv sync

# Of alleen de runtime dependencies
uv pip install -e .
```

### Documentatie lokaal bekijken

```bash
# Activeer de virtual environment (optioneel - uv kan ook zonder)
source .venv/bin/activate

# Start de development server
uv run mkdocs serve

# Of als je de venv geactiveerd hebt:
mkdocs serve
```

Open vervolgens [http://127.0.0.1:8000](http://127.0.0.1:8000) in je browser.

De documentatie wordt automatisch herladen bij wijzigingen.

### Documentatie bouwen

```bash
# Build statische site
uv run mkdocs build

# Output staat in ./site/
```

## Project structuur

```
webtech1/
├── docs/                   # Documentatie content
│   ├── week1/             # Week 1: HTML, CSS, Bootstrap
│   ├── week2/             # Week 2: Python OOP
│   ├── week3/             # Week 3: SQL/Databases
│   ├── week4/             # Week 4: Flask
│   ├── week5/             # Week 5: Flask Forms
│   ├── week6/             # Week 6: Flask + ORM
│   ├── week7a/            # Week 7a: Authentication
│   ├── week7b/            # Week 7b: Refactoring
│   └── projecten/         # Projectopdrachten
├── mkdocs.yml             # MkDocs configuratie
├── pyproject.toml         # Python project configuratie
└── README.md              # Dit bestand
```

## Contribueren

Wijzigingen worden aangeboden als Pull Requests voor review door collega-docenten.

### Workflow

1. Maak een nieuwe branch: `git checkout -b feature/beschrijving`
2. Maak je wijzigingen
3. Test lokaal met `mkdocs serve`
4. Commit: `git commit -m "Beschrijving van wijziging"`
5. Push: `git push origin feature/beschrijving`
6. Maak een Pull Request op GitHub

### Branching strategie

- `main` - productie versie (deployed naar GitHub Pages)
- `feature/*` - nieuwe features/verbeteringen
- PR's voor alle wijzigingen, zelfs kleine fixes

## Dependencies

### Runtime (documentatie)
- `mkdocs` - Static site generator
- `mkdocs-material` - Material Design theme
- `pymdown-extensions` - Markdown extensions
- `mknotebooks` - Jupyter notebook support

### Development
- `ipython` - Interactive Python shell
- `nbdime` - Jupyter notebook diff/merge

Zie `pyproject.toml` voor exacte versies.

## Oude setup (deprecated)

De oude `requirements.txt` wordt niet meer gebruikt. Gebruik `uv` zoals hierboven beschreven.

## Deployment

GitHub Actions deployt automatisch naar GitHub Pages bij een push naar `main`.

Zie `.github/workflows/deploy.yml` voor details.
