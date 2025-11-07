import subprocess
import threading
import yaml
import time
from queue import Queue

class Receiver:
    def __init__(self, config):
        self.config = config
        self.process = None
        self.log_queue = Queue()
        self.running = False

    def start(self):
        if self.running:
            return
        self.running = True
        threading.Thread(target=self._run_stream, daemon=True).start()

    def _run_stream(self):
        while self.running:
            try:
                cmd = [
                    "ffmpeg",
                    "-i", self.config["url"],
                    "-f", "alsa",
                    f"{self.config['soundcard']}"
                ]
                self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                for line in self.process.stdout:
                    self.log_queue.put(line.decode())
                self.process.wait()
            except Exception as e:
                self.log_queue.put(f"Error: {e}")
            time.sleep(5)  # reconnect delay

    def stop(self):
        self.running = False
        if self.process:
            self.process.terminate()

class ReceiverManager:
    def __init__(self):
        self.receivers = {}

    def load_config(self, config_file="configs/default.yaml"):
        with open(config_file) as f:
            data = yaml.safe_load(f)
        for r_id, cfg in data.items():
            self.receivers[r_id] = Receiver(cfg)

    def list_receivers(self):
        return list(self.receivers.keys())

    def start(self, receiver_id):
        if receiver_id in self.receivers:
            self.receivers[receiver_id].start()

    def stop(self, receiver_id):
        if receiver_id in self.receivers:
            self.receivers[receiver_id].stop()

    async def stream_logs(self, receiver_id, websocket):
        if receiver_id in self.receivers:
            while True:
                log = self.receivers[receiver_id].log_queue.get()
                await websocket.send_text(log)
