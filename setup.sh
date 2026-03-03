#!/bin/bash

# Setup script for SHL Assessment Recommendation System

echo "========================================="
echo "  SHL Assessment Recommender Setup"
echo "========================================="

# Check Python version
echo "Checking Python version..."
python --version

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Build vector index
echo "Building vector index..."
cd backend
python embeddings.py

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "To start the backend:"
echo "  cd backend && python main.py"
echo ""
echo "To start the frontend:"
echo "  cd frontend && npm install && npm run dev"
echo ""
