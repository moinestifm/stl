#!/bin/bash
set -euo pipefail

# ensure /dev/snd permissions
if [ -d /dev/snd ]; then
  chown root:audio /dev/snd/* || true
  chmod g+rw /dev/snd/* || true
fi

# copy template if missing (first-run friendly)
if [ ! -f /opt/deva/liquidsoap/tx.liq ] && [ -f /opt/deva/liquidsoap/tx-template.liq ]; then
  cp /opt/deva/liquidsoap/tx-template.liq /opt/deva/liquidsoap/tx.liq
fi

# start control server (Flask) binding to localhost interface
python3 /opt/control/control_server.py &

# start supervisord which runs liquidsoap
exec /usr/bin/supervisord -c /etc/supervisor/supervisord.conf
