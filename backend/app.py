from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from backend.receiver import ReceiverManager

app = FastAPI(title="STL Receiver")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

receiver_manager = ReceiverManager()
receiver_manager.load_config("configs/default.yaml")

@app.get("/receivers")
def list_receivers():
    return receiver_manager.list_receivers()

@app.post("/receivers/start/{receiver_id}")
def start_receiver(receiver_id: str):
    receiver_manager.start(receiver_id)
    return {"status": "started", "receiver": receiver_id}

@app.post("/receivers/stop/{receiver_id}")
def stop_receiver(receiver_id: str):
    receiver_manager.stop(receiver_id)
    return {"status": "stopped", "receiver": receiver_id}

@app.websocket("/ws/logs/{receiver_id}")
async def logs_ws(websocket: WebSocket, receiver_id: str):
    await receiver_manager.stream_logs(receiver_id, websocket)
