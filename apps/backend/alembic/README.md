# Alembic Migrations

This directory contains database migration scripts for the application.

## Creating a New Migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

## Applying Migrations

```bash
alembic upgrade head
```

## Rolling Back Migrations

```bash
alembic downgrade -1
```

For more information about Alembic, see the [official documentation](https://alembic.sqlalchemy.org/).