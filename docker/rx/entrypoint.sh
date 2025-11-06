#!/bin/bash
set -euo pipefail

if [ -d /dev/snd ]; then
  chown root:audio /dev/snd/* || true
  chmod g+rw /dev/snd/* || true
fi

if [ ! -f /opt/deva/liquidsoap/rx.liq ] && [ -f /opt/deva/liquidsoap/rx-template.liq ]; then
  cp /opt/deva/liquidsoap/rx-template.liq /opt/deva/liquidsoap/rx.liq
fi

python3 /opt/control/control_server.py &

exec /usr/bin/supervisord -c /etc/supervisor/supervisord.conf
