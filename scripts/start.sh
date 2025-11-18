#!/bin/bash

echo "🚀 Starting PhD Application Automator..."
echo ""

# Start backend
echo "Starting backend server..."
cd backend
source venv/bin/activate

# Create database tables
echo "Initializing database..."
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"

# Start Flask in background
echo "Starting Flask API server on http://localhost:5000..."
python app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo ""
echo "Starting frontend development server..."
cd ../frontend

# Start React in background
npm start &
FRONTEND_PID=$!

echo ""
echo "✅ Application started successfully!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for interrupt
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

# Wait for processes
wait
