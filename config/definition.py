"""
Schema definition of the hierarchical config files and CLI arguments.
"""
from typing import List
from pydantic import validator
from pydantic.dataclasses import dataclass
from dataclasses import field
from .validate import validate

@dataclass
class Schema:
    addr: str = "0.0.0.0"
    @validator("addr")
    def check_addr(cls, addr: str) -> str:
        return validate.addr(cls,addr)
    port: int = 8000
    @validator("port")
    def check_port(cls, port: int) -> int:
        return validate.port(cls,port)
    eth_api_addresses: List[str] = field(default_factory=lambda: ["http://localhost:5051"])
    @validator("eth_api_addresses")
    def check_eth_api_addresses(cls, eth_api_addresses: List[str]) -> List[str]:
        return validate.eth_api_addresses(cls,eth_api_addresses)
    config: str = "config.yaml"

cli_args = {
    'addr': {
        'args': ["-a", "--addr"],
        'type': str,
        'dest' : 'addr',
        'default' : '0.0.0.0',
        'help' : 'the ip address or domain of your synclink server',
    },
    'port': {
        'args': ["-p", "--port"],
        'type': int,
        'dest' : 'port',
        'default' : 8000,
        'help' : 'the port of your synclink erver',
    },
    'eth_api_addresses': {
        'args': ["-e", "--eth_api_address", "--eth_api_addresses", "--api", "--apis", "--node", "--nodes"],
        'type': str,
        'action': 'append',
        'dest' : 'eth_api_addresses',
        'default' : ["http://127.0.0.1:5051"],
        'help' : 'the http address of your eth api nodes',
    },
    'config': {
        'args': ["-c", "--config"],
        'type': str,
        'dest' : 'config',
        'default' : "config.yaml",
        'help' : 'path to an optional config YAML file',
    },
}