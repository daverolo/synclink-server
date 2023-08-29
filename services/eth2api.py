from urllib.parse import urljoin

import httpx
from apiclient_pydantic import serialize_all_methods

from models.get_block_root_response import GetBlockRootResponse
from models.get_block_v2_response import GetBlockV2Response
from models.get_deposit_contract_response import GetDepositContractResponse
from models.get_fork_schedule_response import GetForkScheduleResponse
from models.get_genesis_response import GetGenesisResponse
from models.get_peer_count_response import GetPeerCountResponse
from models.get_peers_response import GetPeersResponse
from models.get_spec_response import GetSpecResponse
from models.get_state_finality_checkpoints_response import \
    GetStateFinalityCheckpointsResponse
from models.get_syncing_status_response import GetSyncingStatusResponse
from models.get_version_response import GetVersionResponse

from .base_api import API

@serialize_all_methods()
class BeaconAPI(API):
    async def genesis(self) -> GetGenesisResponse:
        return await self.request('/eth/v1/beacon/genesis')

    async def block_root(self, block_id) -> GetBlockRootResponse:
        return await self.request(f"/eth/v1/beacon/blocks/{block_id}/root")

    async def state_finality_checkpoints(self, state_id) -> GetStateFinalityCheckpointsResponse:
        return await self.request(f"/eth/v1/beacon/states/{state_id}/finality_checkpoints")

    async def block(self, block_id) -> GetBlockV2Response:
        return await self.request(f"/eth/v2/beacon/blocks/{block_id}")

    def block_ssz(self, block_id):
        with httpx.stream("GET", urljoin(self.apiUrl, f"/eth/v2/beacon/blocks/{block_id}"), headers={'Accept': 'application/octet-stream'}) as response:
            for chunk in response.iter_bytes():
                yield chunk


@serialize_all_methods()
class ConfigAPI(API):
    async def spec(self) -> GetSpecResponse:
        return await self.request('/eth/v1/config/spec')

    async def deposit_contract(self) -> GetDepositContractResponse:
        return await self.request('/eth/v1/config/deposit_contract')

    async def fork_schedule(self) -> GetForkScheduleResponse:
        return await self.request('/eth/v1/config/fork_schedule')


@serialize_all_methods()
class NodeAPI(API):
    async def health(self):
        return await self.client.get('/eth/v1/node/health')

    async def syncing(self) -> GetSyncingStatusResponse:
        return await self.request('/eth/v1/node/syncing')

    async def version(self) -> GetVersionResponse:
        return await self.request('/eth/v1/node/version')

    async def peers(self) -> GetPeersResponse:
        return await self.request('/eth/v1/node/peers')

    async def peer_count(self) -> GetPeerCountResponse:
        return await self.request('/eth/v1/node/peer_count')


class DebugAPI(API):
    def bacon_state(self, state_id):
        with httpx.stream("GET", urljoin(self.apiUrl, f"/eth/v2/debug/beacon/states/{state_id}"), headers={'Accept': 'application/octet-stream'}) as r:
            for chunk in r.iter_bytes():
                yield chunk


class ETH2API:
    def __init__(self, apiUrl):
        self.apiUrl = apiUrl
        self.beacon = BeaconAPI(self.apiUrl)
        self.config = ConfigAPI(self.apiUrl)
        self.node = NodeAPI(self.apiUrl)
        self.debug = DebugAPI(self.apiUrl)
