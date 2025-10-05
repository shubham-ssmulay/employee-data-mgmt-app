#!/bin/bash

# =========================
# Employee Management System Fullstack
# Runs Backend (FastAPI) + Frontend (Vite) concurrently
# =========================

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Backend...${NC}"
cd backend || exit
# Run backend in background
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 &

BACKEND_PID=$!

echo -e "${BLUE}Starting Frontend...${NC}"
cd ../frontend || exit
npm run dev

# When frontend stops, kill backend
kill $BACKEND_PID

