"""Seed Postgres and MongoDB with benchmark data for every dataset that needs them.

Idempotent: skips a database if it's already loaded.
"""
from __future__ import annotations
import os
import subprocess
import sys
from pathlib import Path
import yaml
import psycopg2
from pymongo import MongoClient

REPO = Path(__file__).resolve().parent.parent
PG_HOST = "127.0.0.1"
PG_PORT = 5432
PG_USER = "shreyashankar"  # superuser on homebrew macOS install
MONGO_URI = "mongodb://localhost:27017/"


def pg_db_exists(name: str) -> bool:
    conn = psycopg2.connect(dbname="postgres", user=PG_USER, host=PG_HOST, port=PG_PORT)
    conn.autocommit = True
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname=%s;", (name,))
        return cur.fetchone() is not None
    finally:
        conn.close()


def pg_load(db_name: str, sql_file: Path) -> None:
    if pg_db_exists(db_name):
        print(f"  pg: {db_name} already exists — skipping")
        return
    print(f"  pg: creating {db_name} and loading {sql_file.name}")
    conn = psycopg2.connect(dbname="postgres", user=PG_USER, host=PG_HOST, port=PG_PORT)
    conn.autocommit = True
    try:
        cur = conn.cursor()
        cur.execute(
            f'CREATE DATABASE "{db_name}" WITH ENCODING=\'UTF8\' '
            "LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0;"
        )
    finally:
        conn.close()
    env = os.environ.copy()
    env["PGCLIENTENCODING"] = "UTF8"
    subprocess.run(
        ["psql", f"-h{PG_HOST}", f"-U{PG_USER}", "-d", db_name, "-f", str(sql_file), "-q"],
        check=True, env=env,
    )


def mongo_db_exists(name: str) -> bool:
    with MongoClient(MONGO_URI) as c:
        return name in c.list_database_names()


def mongo_load(db_name: str, dump_folder: Path) -> None:
    if mongo_db_exists(db_name):
        print(f"  mongo: {db_name} already exists — skipping")
        return
    print(f"  mongo: restoring {db_name} from {dump_folder}")
    subprocess.run(
        ["mongorestore", f"--nsInclude={db_name}.*", str(dump_folder)],
        check=True,
    )


def main() -> None:
    datasets = sorted(p for p in REPO.glob("query_*") if p.is_dir())
    for ds in datasets:
        cfg_path = ds / "db_config.yaml"
        if not cfg_path.exists():
            continue
        cfg = yaml.safe_load(cfg_path.read_text())["db_clients"]
        has_server_db = any(c["db_type"] in ("postgres", "mongo") for c in cfg.values())
        if not has_server_db:
            continue
        print(f"[{ds.name}]")
        for client in cfg.values():
            if client["db_type"] == "postgres":
                sql_file = ds / client["sql_file"]
                if not sql_file.exists():
                    print(f"  SKIP (missing {sql_file})")
                    continue
                pg_load(client["db_name"], sql_file)
            elif client["db_type"] == "mongo":
                dump = ds / client["dump_folder"]
                if not dump.exists():
                    print(f"  SKIP (missing {dump})")
                    continue
                mongo_load(client["db_name"], dump)


if __name__ == "__main__":
    main()
