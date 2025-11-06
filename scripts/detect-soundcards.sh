#!/usr/bin/env bash
echo "ALSA capture devices:"
arecord -l || true
echo
echo "ALSA playback devices:"
aplay -l || true
echo
echo "USB devices:"
lsusb || true
