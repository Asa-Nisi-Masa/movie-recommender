from dotenv import load_dotenv
load_dotenv()
import argparse
import os
from yoyo import read_migrations, get_backend


parser = argparse.ArgumentParser()
parser.add_argument("--rollback", action="store_true")
args = parser.parse_args()

host = os.environ.get("DB_HOST")
name = os.environ.get("DB_NAME")
user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")

backend = get_backend(f"postgresql://{user}:{password}@{host}/{name}")
migrations = read_migrations("./migrations")


with backend.lock():
    if not args.rollback:
        backend.apply_migrations(backend.to_apply(migrations))
    else:
        backend.rollback_migrations(backend.to_rollback(migrations[-1:]))
