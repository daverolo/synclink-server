from fastapi import HTTPException, status, Request
from loguru import logger
from core.node import Node

def validate_response(response, request: Request, node: Node, detail=f"Node did no respond properly"):
    if not response:
        url = ""
        if node and hasattr(node,'url'):
            url = node.url
        logger.debug(f"Response from request {url + request.scope['path']} was '{response}'")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail)
