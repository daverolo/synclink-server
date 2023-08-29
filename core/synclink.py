import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from config.config import config
from core.node import Node

logger.disable("apscheduler")

class SynclinkServer():
    def __init__(self, eth_api_address: Node) -> None:
        self.node = Node(eth_api_address)
        self.ready = None
        self.query_node_job = None

    async def start(self):
        docs_addr = config.addr if config.addr != "0.0.0.0" else "127.0.0.1" 
        docs_port = config.port
        logger.success(f"Synclink Server started, find API docs at http://{docs_addr}:{docs_port}/docs")
        self.scheduler = AsyncIOScheduler()
        self.query_node_job = self.scheduler.add_job(self.query_node, 'interval', seconds=3, max_instances=1)
        self.query_node_job.modify(next_run_time=datetime.datetime.now())
        self.scheduler.start()

    async def query_node(self):
        is_ready = await self.node.is_ready()
        if (is_ready):
            if not self.ready:
                logger.success(f"Upstream node {self.node.url} ready")
            else:
                logger.debug(f"Upstream node {self.node.url} still ready")
            if self.query_node_job.trigger.interval.seconds < 6:
                self.scheduler.reschedule_job(self.query_node_job.id, trigger='interval', seconds=6)
            self.ready = True
        else:
            if self.ready:
                logger.warning(f"Upstream node {self.node.url} not ready anymore")
            elif self.ready is None:
                logger.warning(f"Waiting for upstream node {self.node.url} to get ready")
            else:
                logger.debug(f"Upstream node {self.node.url} not ready, retry in 3 seconds!")
            if self.query_node_job.trigger.interval.seconds > 3:
                self.scheduler.reschedule_job(self.query_node_job.id, trigger='interval', seconds=3)
            self.ready = False

server = SynclinkServer(config.eth_api_address)
