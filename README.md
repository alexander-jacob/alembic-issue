# Alembic Issue

There is an issue with foreign keys and models using `public` as an explicit schema.

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
```bash
docker-compose up -d
```

# Steps to reproduce

Upgrade the database 
```bash
(venv) alex@alex:~/dje/alembic-issue$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> da119d71d931, create-customer-type
INFO  [alembic.runtime.migration] Running upgrade da119d71d931 -> b78942501330, create-customer
INFO  [alembic.runtime.migration] Running upgrade b78942501330 -> 5cd5e42303f2, wtf
```

So far everything went well and as expected. 

Now let's autogenerate another version `alembic revision --autogenerate --message "wtf"`

**Expected:** Alembic generates an empty version with no changes detected.

**Actual:** Alembic detects the following changes:
```bash
(venv) alex@alex:~/alembic-issue$ alembic revision --autogenerate --message "wtf"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected removed foreign key (customer_type_id)(id) on table customer
INFO  [alembic.autogenerate.compare] Detected added foreign key (customer_type_id)(id) on table public.customer
  Generating /home/alex/dje/alembic-issue/alembic/versions/20221125_095053_5cd5e42303f2_wtf.py ...  done
```

- as you can see there is a bug with the inspection when using `public` schema.
- maybe this is due to `public` being the default in `search_path`?
- this is possibly related to https://github.com/sqlalchemy/alembic/issues/519
