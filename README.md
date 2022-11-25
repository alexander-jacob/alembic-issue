# Alembic Issue

# Description


# Setup

**Requirements**
- Linux / Mac
- Python >= 3.6
- docker with docker-compose

**Create virtualenv and install requirements**
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Start postgres container**
You may change the ports in `docker-compose.yaml`

```bash
docker-compose up -d
```

# Notes
Some notes about the setup

Changes to `/alembic.ini`
```ini
# to sort revisions in time based order
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d%%(second).2d_%%(rev)s_%%(slug)s
```

changes to `/alembic/env.py`
```python
context.configure(
    include_schemas=True
)
```
