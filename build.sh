#!/usr/bin/env bash

set -e

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [build.sh] $1"
}

pip install -r requirements.txt

if [ -f "frc_components.db" ]; then
    log "Using existing database from repo"
    cp frc_components.db /tmp/frc_components.db
else
    log "Creating new database and seeding"
    python run_seed.py
    cp frc_components.db /tmp/frc_components.db
fi