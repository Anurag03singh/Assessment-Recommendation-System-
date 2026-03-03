FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY backend/requirements-railway.txt backend/requirements-railway.txt
RUN pip install --no-cache-dir -r backend/requirements-railway.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
