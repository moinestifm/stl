FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    liquidsoap \
    ffmpeg \
    alsa-utils \
    pulseaudio \
    python3 \
    python3-pip \
    supervisor \
    netcat-openbsd \
    curl \
    ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY control_server.py /opt/control/control_server.py
RUN pip3 install flask==2.3.2

COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

WORKDIR /opt/deva
VOLUME [ "/opt/deva/liquidsoap", "/opt/deva/recordings" ]

EXPOSE 8081 1235

RUN chmod +x /usr/local/bin/entrypoint.sh /opt/control/control_server.py

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
