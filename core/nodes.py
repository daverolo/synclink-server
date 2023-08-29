from typing import List
from models.get_state_finality_checkpoints_response_data import GetStateFinalityCheckpointsResponseData

from utils.list import async_filter

from core.node import Node


class Nodes:
    def __init__(self, nodes: List[str]) -> None:
        self.nodes = [Node(n) for n in set(nodes)]

    async def get_readies(self) -> List[Node]:
        async def check_is_ready(node: Node):
            is_ready = await node.is_ready()

            return is_ready

        ready_nodes = [i async for i in async_filter(check_is_ready, self.nodes)]

        return ready_nodes
