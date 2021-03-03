echo "Initialize PostgreSQL"
psql -U postgres -d postgres -c "initdb;";

echo "Create PostgreSQL role"
psql -U postgres -d postgres -c "CREATE ROLE ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}' WITH LOGIN CREATEDB;";

echo "Create database"
psql -U postgres -d postgres -c "CREATE DATABASE ${POSTGRES_DB} WITH OWNER ${POSTGRES_USER};";

echo "Install database extensions"
psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -c "CREATE EXTENSION pg_trgm unaccent;";