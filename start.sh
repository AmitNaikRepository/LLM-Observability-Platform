#!/bin/bash

echo "=========================================="
echo "  LLM Observability Platform - Startup"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env with your GROQ_API_KEY"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running!"
    echo "Please start Docker Desktop"
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Start Docker services
echo "🚀 Starting observability stack..."
echo "   - Jaeger (traces)"
echo "   - Prometheus (metrics)"
echo "   - Grafana (dashboards)"
echo "   - OpenTelemetry Collector"
echo ""

docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if containers are running
RUNNING=$(docker-compose ps --services --filter "status=running" | wc -l)
TOTAL=$(docker-compose ps --services | wc -l)

if [ "$RUNNING" -eq "$TOTAL" ]; then
    echo "✅ All services are running!"
else
    echo "⚠️  Warning: Some services may not be running"
    docker-compose ps
fi

echo ""
echo "=========================================="
echo "  Services Ready!"
echo "=========================================="
echo ""
echo "📊 Access your observability tools:"
echo ""
echo "  Jaeger UI:       http://localhost:16686"
echo "  Prometheus:      http://localhost:9090"
echo "  Grafana:         http://localhost:3000 (admin/admin)"
echo "  API Docs:        http://localhost:8000/docs"
echo "  Metrics:         http://localhost:8001/metrics"
echo ""
echo "=========================================="
echo ""
echo "🚀 Now starting FastAPI application..."
echo ""
echo "Run: python main.py"
echo ""
echo "Then test with:"
echo "  curl -X POST http://localhost:8000/api/chat \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"prompt\": \"Hello!\", \"max_tokens\": 50}'"
echo ""
