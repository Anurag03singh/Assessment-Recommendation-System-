@echo off
REM Setup script for SHL Assessment Recommendation System

echo =========================================
echo   SHL Assessment Recommender Setup
echo =========================================

REM Check Python version
echo Checking Python version...
python --version

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Build vector index
echo Building vector index...
cd backend
python embeddings.py
cd ..

echo.
echo =========================================
echo   Setup Complete!
echo =========================================
echo.
echo To start the backend:
echo   cd backend ^&^& python main.py
echo.
echo To start the frontend:
echo   cd frontend ^&^& npm install ^&^& npm run dev
echo.
pause
