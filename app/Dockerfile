FROM python:3.12-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y liquidsoap pulseaudio alsa-utils ffmpeg curl netcat-openbsd && \
    apt-get clean

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "panel.py"]
