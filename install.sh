#!/bin/bash
# =============================================================================
# AI Receptionist Enterprise — Installation Script
# =============================================================================
# Usage: ./install.sh
# =============================================================================

set -e

echo "🚀 AI Receptionist Enterprise — Installation"
echo "=========================================="

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed."; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose is required but not installed."; exit 1; }

# Setup environment
echo "📋 Setting up environment..."
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env with your actual API keys before starting."
fi

# Start services
echo "🐳 Starting Docker services..."
cd infra
docker compose up -d

# Wait for DB
echo "⏳ Waiting for database..."
sleep 5

# Run migrations
echo "🗄️  Running database migrations..."
docker compose exec api alembic upgrade head || echo "⚠️  Alembic migrations not yet created. Using init_db() instead."

# Health check
echo "🏥 Checking API health..."
curl -s http://localhost/api/v1/health || echo "⚠️  API not yet ready. Try again in 30 seconds."

echo ""
echo "✅ Installation complete!"
echo ""
echo "📱 Frontend: http://localhost"
echo "📚 API Docs: http://localhost/api/v1/docs"
echo "📊 Metrics:  http://localhost/api/v1/metrics"
echo ""
echo "🔧 Next steps:"
echo "   1. Edit backend/.env with your API keys"
echo "   2. Restart: docker compose restart api"
echo "   3. Run tests: cd backend && pytest"
