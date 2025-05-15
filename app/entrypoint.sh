#!/bin/sh

# Uscita immediata se un comando fallisce
set -e

# Verifica la presenza delle variabili d'ambiente necessarie
if [ -z "$DB_HOST" ] || [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_DB" ]; then
  echo ">>> ERRORE: Le variabili d'ambiente DB_HOST, POSTGRES_USER, POSTGRES_DB devono essere impostate."
  exit 1
fi

echo ">>> In attesa che il database ($DB_HOST) sia pronto..."

if [ -n "$POSTGRES_PASSWORD" ]; then
    export PGPASSWORD="$POSTGRES_PASSWORD"
fi

counter=0
max_attempts=60
while ! pg_isready -h "$DB_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -q; do
  counter=$((counter+1))
  if [ $counter -ge $max_attempts ]; then
    echo ">>> ERRORE: Timeout - Il database non è diventato pronto dopo $max_attempts tentativi."
    if [ -n "$POSTGRES_PASSWORD" ]; then
        unset PGPASSWORD
    fi
    exit 1
  fi
  echo ">>> Database non ancora pronto (Tentativo $counter/$max_attempts). Attendo 2 secondi..."
  sleep 2
done

echo ">>> Il database è pronto."

if [ -n "$POSTGRES_PASSWORD" ]; then
    unset PGPASSWORD
fi

# Esegui le migrazioni del database Django (SOLO migrate, non makemigrations)
echo ">>> Applicazione delle migrazioni del database..."
python manage.py migrate --noinput

# Raccogli i file statici
echo ">>> Raccolta dei file statici..."
python manage.py collectstatic --noinput --clear # --clear rimuove file vecchi

echo ">>> Avvio del server Gunicorn (comando passato da docker-compose)..."
# Esegui il comando passato all'entrypoint (es. gunicorn)
exec "$@"
