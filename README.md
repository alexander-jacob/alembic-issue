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

```bash
make up
```

**some notes**
- changes in `/alembic.ini` and `/alembic/env.py`  are commented

# how to reproduce the issue

Create model `CustomerType` in `issue/models.py`

```python
class CustomerType(Base):
    __tablename__ = "customer_type"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    code = Column(String(32), comment="customer type code", nullable=False)
```

Generate the revision for `CustomerType`
```bash
(venv) alex@alex:~/alembic-issue$ alembic revision --autogenerate --message "create-customer-type"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'customer_type'
  Generating /home/alex/dje/alembic-issue/alembic/versions/20221125_092651_da119d71d931_create_customer_type.py ...  done
```

Upgrade the database 
```bash
(venv) alex@alex:~/alembic-issue$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> da119d71d931, create-customer-typ
```

Then create a model `Customer` **with a foreign key** to `CustomerType`
```python
class Customer(Base):
    __tablename__ = "customer"
    __table_args__ = {"schema": "public"}

    primary_key = Column(String(32), primary_key=True, comment="UID")
    first_name = Column(String(100), comment="First name", nullable=False)
    last_name = Column(String(100), comment="Last name", nullable=False)
    customer_type_id = Column(Integer, ForeignKey("public.customer_type.id"))
```

Generate the revision for `Customer`
```bash
(venv) alex@alex:~/alembic-issue$ alembic revision --autogenerate --message "create-customer"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'customer'
INFO  [alembic.ddl.postgresql] Detected sequence named 'customer_type_id_seq' as owned by integer column 'customer_type(id)', assuming SERIAL and omitting
  Generating /home/alex/dje/alembic-issue/alembic/versions/20221125_094823_b78942501330_create_customer.py ...  done
```

Upgrade the database 
```bash
(venv) alex@alex:~/alembic-issue$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade da119d71d931 -> b78942501330, create-customer
```

**So far everything went well and as expected.** 

And not the problems start. Let's generate another migration:  

```bash
(venv) alex@alex:~/alembic-issue$ alembic revision --autogenerate --message "wtf"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected removed foreign key (customer_type_id)(id) on table customer
INFO  [alembic.autogenerate.compare] Detected added foreign key (customer_type_id)(id) on table public.customer
  Generating /home/alex/dje/alembic-issue/alembic/versions/20221125_095053_5cd5e42303f2_wtf.py ...  done
```

As you can see there is a bug with the inspection when using schemas.