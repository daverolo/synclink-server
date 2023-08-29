import random
import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from config.config import config
from core.nodes import Nodes

logger.disable("apscheduler")

class SynclinkServer():
    def __init__(self, eth_api_addresses: Nodes) -> None:
        self.eth_api_addresses = eth_api_addresses
        self.nodes = Nodes(eth_api_addresses)
        self.selected_ready_node = None
        self.find_ready_node_job = None

    async def start(self):
        docs_addr = config.addr if config.addr != "0.0.0.0" else "127.0.0.1" 
        docs_port = config.port
        logger.success(f"Synclink Server started, find API docs at http://{docs_addr}:{docs_port}/docs")
        self.scheduler = AsyncIOScheduler()
        self.find_ready_node_job = self.scheduler.add_job(self.find_ready_node, 'interval', seconds=5, max_instances=1)
        self.find_ready_node_job.modify(next_run_time=datetime.datetime.now())
        self.scheduler.start()

    async def find_ready_node(self):

        if self.selected_ready_node:
            logger.debug(f"Checking upstream node")
            if await self.selected_ready_node.is_ready():
                logger.debug(f"Choosen upstream node {self.selected_ready_node.url} still ready")
                if self.find_ready_node_job.trigger.interval.seconds < 15:
                    self.scheduler.reschedule_job(self.find_ready_node_job.id, trigger='interval', seconds=15)
                return True
            else:
                logger.warning(f"Choosen upstream node {self.selected_ready_node.url} not ready anymore")
                if self.find_ready_node_job.trigger.interval.seconds > 5:
                    self.scheduler.reschedule_job(self.find_ready_node_job.id, trigger='interval', seconds=5)
                self.selected_ready_node = None

        logger.info('Searching for at least one ready node...')

        ready_nodes = await self.nodes.get_readies()
        if not len(ready_nodes):
            logger.warning('No ready node found! Will try in 5 sec..')
            return False
        
        logger.success(f"{str(len(ready_nodes))} ready node(s) found.")

        self.selected_ready_node = random.choice(ready_nodes)

        logger.success(f"Node {self.selected_ready_node.url} choosen as upstream")


server = SynclinkServer(config.eth_api_addresses)
