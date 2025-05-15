#!/usr/bin/env bash
set -euo pipefail

# Spinner function to show progress (mantieni se ti piace)
task_spinner() {
  # ... (codice dello spinner) ...
}

# Run a docker or django command with sudo, spinner, and error handling (mantieni se usi sudo)
task() {
  local description="$1"
  shift
  echo "$description"
  # Rimuovi sudo se non necessario (es. se l'utente è già nel gruppo docker)
  sudo "$@" &
  local pid=$!
  task_spinner "$pid"
  wait "$pid"
  local status=$?
  if [ "$status" -ne 0 ]; then
    echo "❌ Errore durante: $description"
    exit "$status"
  else
    echo "✅ Completato: $description"
  fi
}

# Move to script directory (project root)
cd "$(dirname "$0")"

# Pull delle ultime modifiche dal repository (se usi Git)
# echo "🔄 Pull delle ultime modifiche..."
# git pull origin main # O il branch che usi

# Stop dei container esistenti (SENZA --volumes per preservare i dati del DB)
task "🔻 Stop dei container" docker compose down --remove-orphans

# Pruning (USA CON CAUTELA - Rimuovono risorse Docker non usate sull'intero sistema!)
# Commenta queste righe se non sei sicuro o se hai altri progetti Docker in esecuzione
# task "🧹 Prune sistema Docker (immagini non usate, etc.)" docker system prune -f
# task "🧹 Prune volumi Docker non usati" docker volume prune -f

# Ricostruzione e avvio dei servizi
task "🏗️  Ricostruzione delle immagini (se necessario) e avvio servizi..." docker compose up -d --build

# Mostra i log del servizio web per qualche secondo (opzionale)
# echo "🪵  Mostra i log recenti del servizio web..."
# docker compose logs --tail=20 web
# sleep 5

# Fine script
echo "🎉 Aggiornamento e avvio completati!"
echo "ℹ️  L'applicazione dovrebbe essere accessibile tra poco."
echo "ℹ️  Controlla i log con: docker compose logs -f web"
