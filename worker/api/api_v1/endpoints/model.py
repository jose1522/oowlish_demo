from fastapi import APIRouter, WebSocket

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint for receiving Youtube link videos and sending back a summary of it."""
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
