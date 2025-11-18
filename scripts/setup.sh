#!/bin/bash

echo "🚀 Setting up PhD Application Automator..."
echo ""

# Backend setup
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Backend setup complete!"
echo ""

# Frontend setup
echo "📦 Setting up frontend..."
cd ../frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete!"
echo ""

cd ..

echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "  1. Edit backend/.env with your configuration (if needed)"
echo "  2. Run ./scripts/start.sh to start the application"
echo ""
