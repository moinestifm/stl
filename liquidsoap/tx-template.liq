####################################################
# DEVA-STL TX Liquidsoap template
# Supports: ALSA, PulseAudio, HTTP/Icecast, RTP (via ffmpeg relay)
# The web control panel writes a concrete file based on this template.
####################################################

set("log.file", false)
set("log.stdout", true)
set("log.level", 3)
set("frame.size", 4096)
set("sampling.rate", 48000)
set("harbor.bind_addr","0.0.0.0")
set("server.telnet", true)
set("server.telnet.port", 1234)
set("server.telnet.password", "please_change_this_password")

# --- configuration variables (replace with your values in the web UI)
# available variables expected to be replaced by web UI:
# HTTP_SRC, ALSA_DEV, PULSE_DEV, RTP_LOCAL_RELAY_HTTP, ICECAST_HOST, ICECAST_PORT, ICECAST_PASS, ICECAST_MOUNT

# default fallbacks
HTTP_SRC = "{{HTTP_SRC}}"
ALSA_DEV = "{{ALSA_DEV}}"
PULSE_DEV = "{{PULSE_DEV}}"
RTP_RELAY = "{{RTP_RELAY}}"           # local http relay that ffmpeg may provide: e.g. http://127.0.0.1:8700/relay
ICECAST_HOST = "{{ICECAST_HOST}}"
ICECAST_PORT = {{ICECAST_PORT}}
ICECAST_PASS = "{{ICECAST_PASS}}"
ICECAST_MOUNT = "{{ICECAST_MOUNT}}"

# helper constructors
def mk_http(url)
  if url == "" then null()
  else mksafe(input.http(url, buffer=5.))
  end
end

def mk_alsa(dev)
  if dev == "" then null()
  else
    # explicitly set channels/rate if needed
    mksafe(input.alsa(device=dev, channels=2, rate=48000, bufferize=true))
  end
end

def mk_pulse(dev)
  if dev == "" then null()
  else mksafe(input.pulseaudio(device=dev))
  end
end

# assemble sources
http_src = mk_http(HTTP_SRC)
alsa_src = mk_alsa(ALSA_DEV)
pulse_src = mk_pulse(PULSE_DEV)
rtp_src = mk_http(RTP_RELAY) # use ffmpeg to create relay if needed

# choose priority: local hardware > RTP > HTTP
main_src = fallback(track_sensitive=false, [alsa_src, pulse_src, rtp_src, http_src])

# normalization & limiter
vol = normalize:0.95(max=1., min=-1.)(compress(threshold=-15., ratio=3., s = main_src))

# optional recording of local stream (rotate externally as needed)
# output.file(%wav, "/opt/deva/recordings/tx_current.wav", vol)

# outputs
# If icecast config is provided, publish
if ICECAST_HOST != "" then
  output.icecast(%mp3, host=ICECAST_HOST, port=ICECAST_PORT, password=ICECAST_PASS, mount=ICECAST_MOUNT, vol)
end

# local monitor to ALSA (so you can attach hardware)
output.alsa(device="default", vol)
