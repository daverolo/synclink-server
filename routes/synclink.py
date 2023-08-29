import core.synclink
from core.config import Config
from fastapi import APIRouter, Header, Response
from validators.content_type import ContentTypeJSON, validate_content_type


synclink_router = APIRouter()

synclink_server = core.synclink.server


@synclink_router.get("/v1/config", tags=["Synclink"], response_model=Config)
async def handle_synclink_v1_config(content_type: str = Header(default=ContentTypeJSON)):
    validate_content_type(content_type, [ContentTypeJSON])
    if not synclink_server.selected_ready_node or not synclink_server.selected_ready_node.config:
        return Response(status_code=503)
    
    return synclink_server.selected_ready_node.config


@synclink_router.get("/v1/ready", tags=["Synclink"], responses={200: {"description": "Synclink server is ready to use with synclink client.", "content": None}, 503: {"description": "Synclink server is not ready yet.", }})
async def handle_synclink_v1_ready_status():
    if not synclink_server.selected_ready_node:
        return Response(status_code=503)
    
    is_ready = await synclink_server.selected_ready_node.is_ready()

    if (is_ready):
        return Response(status_code=200)

    return Response(status_code=503)
