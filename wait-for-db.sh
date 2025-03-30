#!/bin/bash
set -e

host="dpt-manager-db"
port="5432"

until nc -z "$host" "$port"; do
  >&2 echo "Postgres no está listo - esperando..."
  sleep 1
done

>&2 echo "Postgres está listo - iniciando la aplicación"
exec python app.py