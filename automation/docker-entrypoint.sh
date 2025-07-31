#!/bin/bash
set -e

# Docker entrypoint script for AWS Ontology Monitoring

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Initialize directories
mkdir -p automation/logs automation/reports monitoring

# Set default configuration if not provided
if [ ! -f "automation/config.json" ]; then
    log "Creating default configuration..."
    python automation/schedule_monitoring.py --create-config --config automation/config.json
fi

# Handle different run modes
case "${1:-daemon}" in
    "daemon")
        log "Starting scheduler daemon..."
        exec python automation/schedule_monitoring.py --start-daemon --config automation/config.json
        ;;
    "daily")
        log "Running daily monitoring task..."
        exec python automation/schedule_monitoring.py --run-once daily --config automation/config.json
        ;;
    "weekly")
        log "Running weekly report task..."
        exec python automation/schedule_monitoring.py --run-once weekly --config automation/config.json
        ;;
    "monthly")
        log "Running monthly quality check..."
        exec python automation/schedule_monitoring.py --run-once monthly --config automation/config.json
        ;;
    "quarterly")
        log "Running quarterly review..."
        exec python automation/schedule_monitoring.py --run-once quarterly --config automation/config.json
        ;;
    "test")
        log "Running test suite..."
        exec make test-all
        ;;
    "monitor")
        log "Running AWS change monitoring..."
        exec make monitor-changes
        ;;
    "bash")
        log "Starting interactive bash shell..."
        exec /bin/bash
        ;;
    *)
        log "Executing custom command: $@"
        exec "$@"
        ;;
esac 