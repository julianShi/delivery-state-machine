from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List
import json
import logging
from datetime import datetime

router = APIRouter()
logger = logging.getLogger(__name__)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        # Map of delivery_id to list of active connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, delivery_id: str):
        await websocket.accept()
        if delivery_id not in self.active_connections:
            self.active_connections[delivery_id] = []
        self.active_connections[delivery_id].append(websocket)
        logger.info(f"New WebSocket connection for delivery {delivery_id}")

    def disconnect(self, websocket: WebSocket, delivery_id: str):
        if delivery_id in self.active_connections:
            self.active_connections[delivery_id].remove(websocket)
            if not self.active_connections[delivery_id]:
                del self.active_connections[delivery_id]
        logger.info(f"WebSocket disconnected for delivery {delivery_id}")

    async def broadcast_to_delivery(self, delivery_id: str, message: dict):
        if delivery_id in self.active_connections:
            for connection in self.active_connections[delivery_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message to WebSocket: {e}")

manager = ConnectionManager()

@router.websocket("/delivery/{delivery_id}")
async def websocket_delivery_endpoint(websocket: WebSocket, delivery_id: str):
    """WebSocket endpoint for real-time delivery updates"""
    await manager.connect(websocket, delivery_id)
    try:
        while True:
            # Keep connection alive and handle any incoming messages
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                # Handle any client messages if needed
                logger.info(f"Received message for delivery {delivery_id}: {message}")
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received for delivery {delivery_id}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, delivery_id)
    except Exception as e:
        logger.error(f"WebSocket error for delivery {delivery_id}: {e}")
        manager.disconnect(websocket, delivery_id)

# Helper function to broadcast delivery updates
async def broadcast_delivery_update(delivery_id: str, status: str, details: dict = None):
    """Broadcast delivery status update to all connected clients"""
    message = {
        "type": "delivery_update",
        "delivery_id": delivery_id,
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
        "details": details or {}
    }
    await manager.broadcast_to_delivery(delivery_id, message) 