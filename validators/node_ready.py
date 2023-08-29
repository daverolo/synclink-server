from fastapi import HTTPException, status
from core.node import Node


def validate_node_ready(node: Node, detail=f"Node not initialized, currently syncing or having issues"):
    if not node.ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail)
