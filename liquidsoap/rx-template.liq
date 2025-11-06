####################################################
# DEVA-STL RX Liquidsoap template
# Receives: HTTP/Icecast, optional local RTP relay, outputs to ALSA and local icecast monitor
####################################################

set("log.file", false)
set("log.stdout", true)
set("log.level", 3)
set("frame.size", 4096)
set("sampling.rate", 48000)
set("server.telnet", true)
set("server.telnet.port", 1235)
set("server.telnet.password", "please_change_rx_pass")

RX_HTTP_SRC = "{{RX_HTTP_SRC}}"
RX_RTP_RELAY = "{{RX_RTP_RELAY}}"
RX_ALSA_DEV = "{{RX_ALSA_DEV}}"
RX_MON_ICECAST_PORT = {{RX_MON_ICECAST_PORT}}

def mk_http(url)
  if url == "" then null()
  else mksafe(input.http(url, buffer=5.))
  end
end

in_http = mk_http(RX_HTTP_SRC)
in_relay = mk_http(RX_RTP_RELAY)

source = fallback(track_sensitive=false, [in_relay, in_http])

# record locally and rotate externally
output.file(%wav, "/opt/deva/recordings/rx_current.wav", source)

# output to local device
output.alsa(device=RX_ALSA_DEV, source)

# small monitor HTTP/Icecast for local inspection (optional)
output.icecast(%mp3, host="0.0.0.0", port=RX_MON_ICECAST_PORT, password="monitor_pass", mount="/rx_local.mp3", source)
