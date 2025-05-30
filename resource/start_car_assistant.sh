#!/bin/bash

# Verzeichnis deiner Anwendung
APP_DIR="/home/tgrah/git/car-assistant"
cd "$APP_DIR" || exit 1

# Prüfe Netzwerkverbindung (z. B. zu github.com)
echo "Prüfe Internetverbindung..."
if ping -c 1 github.com &> /dev/null; then
    echo "Internetverbindung vorhanden. Prüfe auf Updates..."

    # Git-Status prüfen
    git fetch
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse origin/main)

    if [ "$LOCAL" != "$REMOTE" ]; then
        echo "Update verfügbar – führe Pull aus..."
        git pull
        python3 src/update.py
    else
        echo "Bereits aktuell."
    fi
else
    echo "Keine Internetverbindung – überspringe Git-Update."
fi

# Starte Hauptprogramm immer
echo "Starte car assistant..."
python3 src/main.py
