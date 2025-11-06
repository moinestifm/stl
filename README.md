# STL — Liquidsoap TX/RX with Web Control (Docker)

Production-ready prototype for a cross-platform, Dockerized STL (TX/RX) system using Liquidsoap,
FFmpeg and a lightweight web control panel.

## Features
- TX & RX containers with Liquidsoap handling ALSA / Pulse / HTTP / RTP inputs.
- Small Flask control server in TX/RX to allow secure reloads and config writes.
- Web control panel (Express + React) to edit Liquidsoap configs and restart services.
- Multi-arch CI template (GitHub Actions) for building images for x86_64 and arm64 (Raspberry Pi).
- Designed for USB soundcards, Raspberry Pi, mini PCs, laptops, servers.

## Quickstart (Linux)
1. Clone the repo and edit configs:
   ```bash
   git clone https://github.com/moinestifm/stl
   cd stl
