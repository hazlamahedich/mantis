#!/bin/bash

set -e

echo "Starting Mantis Backend..."

# Function to wait for PostgreSQL to be ready
wait_for_postgres() {
    local host="${DB_HOST:-db}"
    local port="${DB_PORT:-5432}"
    local max_attempts=30
    local attempt=0

    echo "Waiting for PostgreSQL at ${host}:${port}..."

    while [ $attempt -lt $max_attempts ]; do
        if nc -z "$host" "$port" 2>/dev/null; then
            echo "PostgreSQL is ready!"
            return 0
        fi
        attempt=$((attempt + 1))
        echo "Attempt $attempt/$max_attempts: PostgreSQL not ready yet..."
        sleep 2
    done

    echo "ERROR: PostgreSQL did not become ready within $max_attempts attempts"
    return 1
}

# Run Alembic migrations if in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker"

    # Wait for database to be ready
    wait_for_postgres || exit 1

    # Run Alembic migrations
    echo "Running Alembic migrations..."
    uv run alembic upgrade head || {
        echo "ERROR: Alembic migration failed"
        exit 1
    }
    echo "Migrations completed successfully!"

    # Start the FastAPI application
    echo "Starting FastAPI application..."
    fastapi dev app/main.py --host 0.0.0.0 --port 8000 --reload &
    python watcher.py
else
    echo "Running locally with uv"

    # For local development, migrations should be run manually
    echo "Skipping migrations in local mode (run 'uv run alembic upgrade head' manually)"

    # Start the FastAPI application
    uv run fastapi dev app/main.py --host 0.0.0.0 --port 8000 --reload &
    uv run python watcher.py
fi

wait
