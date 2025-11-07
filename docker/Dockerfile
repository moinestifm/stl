FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg alsa-utils nodejs npm git \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Copy backend
COPY backend/ ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy frontend and build
COPY frontend/ ./frontend/
RUN cd frontend && npm install && npm run build

# Copy configs
COPY configs/ ./configs/

# Expose API
EXPOSE 8000

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
