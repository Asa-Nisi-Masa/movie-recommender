#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE db;
    \connect db;
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION cosine_sim;
EOSQL

psql -d db -f db.sql
