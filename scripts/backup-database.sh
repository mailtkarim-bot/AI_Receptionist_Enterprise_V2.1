#!/bin/bash
# =============================================================================
# AI Receptionist Enterprise — Automated Database Backup Script
# =============================================================================
# Usage: ./backup-database.sh [full|wal|redis]
# 
# Features:
# - PostgreSQL full backup (pg_dump) to S3
# - WAL archive continuous backup
# - Redis RDB snapshot backup
# - Encryption at rest (AES-256 via aws s3 server-side)
# - Retention policy enforcement
# - Slack/email notification on failure
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# CONFIGURATION (override via environment variables)
# ---------------------------------------------------------------------------
BACKUP_TYPE="${1:-full}"           # full | wal | redis
S3_BUCKET="${S3_BUCKET:-s3://ai-receptionist-backups-prod}"
DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-ai_receptionist}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-}"
REDIS_HOST="${REDIS_HOST:-redis}"
REDIS_PORT="${REDIS_PORT:-6379}"
REDIS_PASSWORD="${REDIS_PASSWORD:-}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
SLACK_WEBHOOK="${SLACK_WEBHOOK:-}"
EMAIL_ALERT="${EMAIL_ALERT:-}"
LOG_FILE="${LOG_FILE:-/var/log/db_backup.log}"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/tmp/backups"
mkdir -p "$BACKUP_DIR"

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

notify_error() {
    local message="$1"
    log "ERROR: $message"

    if [[ -n "$SLACK_WEBHOOK" ]]; then
        curl -s -X POST -H 'Content-type: application/json'             --data "{"text":"🚨 DB Backup Failed: $message"}"             "$SLACK_WEBHOOK" || true
    fi

    if [[ -n "$EMAIL_ALERT" ]]; then
        echo "$message" | mail -s "[ALERT] DB Backup Failed" "$EMAIL_ALERT" || true
    fi
}

# ---------------------------------------------------------------------------
# POSTGRESQL FULL BACKUP
# ---------------------------------------------------------------------------
backup_postgres_full() {
    log "Starting PostgreSQL full backup..."

    local backup_file="pg_${DB_NAME}_${TIMESTAMP}.sql.gz"
    local s3_path="$S3_BUCKET/postgres/full/"

    # Run pg_dump with compression
    PGPASSWORD="$DB_PASSWORD" pg_dump         -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"         --no-owner --no-privileges         | gzip > "$BACKUP_DIR/$backup_file"

    # Verify backup integrity
    if ! gzip -t "$BACKUP_DIR/$backup_file" 2>/dev/null; then
        notify_error "Backup file $backup_file is corrupted"
        exit 1
    fi

    # Upload to S3 with encryption
    aws s3 cp "$BACKUP_DIR/$backup_file" "$s3_path"         --storage-class STANDARD_IA         --server-side-encryption AES256         --metadata "backup-type=full,db-name=$DB_NAME,timestamp=$TIMESTAMP"

    # Verify upload
    aws s3 ls "$s3_path$backup_file" > /dev/null || {
        notify_error "Failed to verify S3 upload for $backup_file"
        exit 1
    }

    # Cleanup local file
    rm -f "$BACKUP_DIR/$backup_file"

    log "PostgreSQL full backup completed: $backup_file"
}

# ---------------------------------------------------------------------------
# WAL ARCHIVE BACKUP (continuous)
# ---------------------------------------------------------------------------
backup_wal() {
    log "Starting WAL archive backup..."

    # This script is typically called by PostgreSQL archive_command
    # For manual WAL backup, use pg_basebackup or WAL-G

    local wal_file="${1:-}"
    if [[ -z "$wal_file" ]]; then
        log "WAL backup requires a WAL file path. Use with PostgreSQL archive_command."
        return 0
    fi

    local s3_path="$S3_BUCKET/postgres/wal/"

    # Compress and upload WAL segment
    gzip -c "$wal_file" | aws s3 cp - "$s3_path$(basename $wal_file).gz"         --server-side-encryption AES256

    log "WAL archive uploaded: $(basename $wal_file)"
}

# ---------------------------------------------------------------------------
# REDIS RDB SNAPSHOT BACKUP
# ---------------------------------------------------------------------------
backup_redis() {
    log "Starting Redis RDB snapshot backup..."

    local backup_file="redis_${TIMESTAMP}.rdb.gz"
    local s3_path="$S3_BUCKET/redis/"

    # Trigger BGSAVE and wait for completion
    if [[ -n "$REDIS_PASSWORD" ]]; then
        redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" -a "$REDIS_PASSWORD" BGSAVE
    else
        redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" BGSAVE
    fi

    # Wait for BGSAVE to complete (poll every 2s, max 60s)
    local waited=0
    while true; do
        if [[ -n "$REDIS_PASSWORD" ]]; then
            local lastsave=$(redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" -a "$REDIS_PASSWORD" LASTSAVE)
        else
            local lastsave=$(redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" LASTSAVE)
        fi

        if [[ "$lastsave" -ge $(date +%s) ]]; then
            break
        fi

        sleep 2
        waited=$((waited + 2))
        if [[ $waited -ge 60 ]]; then
            notify_error "Redis BGSAVE timeout after 60 seconds"
            exit 1
        fi
    done

    # Compress and upload RDB file
    # Note: In Docker, RDB is at /data/dump.rdb
    gzip -c "/data/dump.rdb" > "$BACKUP_DIR/$backup_file" 2>/dev/null || {
        # Fallback: use redis-cli --rdb
        if [[ -n "$REDIS_PASSWORD" ]]; then
            redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" -a "$REDIS_PASSWORD" --rdb "$BACKUP_DIR/redis_${TIMESTAMP}.rdb"
        else
            redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" --rdb "$BACKUP_DIR/redis_${TIMESTAMP}.rdb"
        fi
        gzip "$BACKUP_DIR/redis_${TIMESTAMP}.rdb"
        mv "$BACKUP_DIR/redis_${TIMESTAMP}.rdb.gz" "$BACKUP_DIR/$backup_file"
    }

    aws s3 cp "$BACKUP_DIR/$backup_file" "$s3_path"         --storage-class STANDARD_IA         --server-side-encryption AES256

    rm -f "$BACKUP_DIR/$backup_file"

    log "Redis RDB backup completed: $backup_file"
}

# ---------------------------------------------------------------------------
# RETENTION POLICY ENFORCEMENT
# ---------------------------------------------------------------------------
enforce_retention() {
    log "Enforcing retention policy ($RETENTION_DAYS days)..."

    local cutoff_date=$(date -d "$RETENTION_DAYS days ago" +%Y%m%d 2>/dev/null || date -v-${RETENTION_DAYS}d +%Y%m%d)

    # Delete old PostgreSQL backups
    aws s3 ls "$S3_BUCKET/postgres/full/" | while read -r line; do
        local file_date=$(echo "$line" | awk '{print $1}' | tr -d '-')
        local file_name=$(echo "$line" | awk '{print $4}')
        if [[ "$file_date" < "$cutoff_date" ]]; then
            aws s3 rm "$S3_BUCKET/postgres/full/$file_name"
            log "Deleted old backup: $file_name"
        fi
    done

    # Delete old Redis backups
    aws s3 ls "$S3_BUCKET/redis/" | while read -r line; do
        local file_date=$(echo "$line" | awk '{print $1}' | tr -d '-')
        local file_name=$(echo "$line" | awk '{print $4}')
        if [[ "$file_date" < "$cutoff_date" ]]; then
            aws s3 rm "$S3_BUCKET/redis/$file_name"
            log "Deleted old Redis backup: $file_name"
        fi
    done
}

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
main() {
    log "=== Backup started: $BACKUP_TYPE ==="

    case "$BACKUP_TYPE" in
        full)
            backup_postgres_full
            backup_redis
            enforce_retention
            ;;
        wal)
            backup_wal "$2"
            ;;
        redis)
            backup_redis
            ;;
        *)
            echo "Usage: $0 [full|wal|redis]"
            exit 1
            ;;
    esac

    log "=== Backup completed successfully ==="
}

main "$@"
