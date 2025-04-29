import aiohttp
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
from .connector import get_connector


DEFAULT_PORT = 8006


async def api_request(
        asset: Asset,
        asset_config: dict,
        config: dict,
        uri: str) -> dict:
    address = config.get('address')
    if not address:
        address = asset.name
    port = config.get('port', DEFAULT_PORT)
    ssl = config.get('ssl', False)

    username = asset_config.get('username')
    realm = asset_config.get('realm', 'pam')
    token_id = asset_config.get('token_id')
    token = asset_config.get('secret')
    if None in (username, realm, token_id, token):
        raise CheckException('missing credentials')

    headers = {
        'Authorization': f'PVEAPIToken={username}@{realm}!{token_id}={token}'
    }
    base_url = f'https://{address}:{port}'
    url = f'{base_url}/api2/json/json/cluster/status'
    async with aiohttp.ClientSession(connector=get_connector()) as session:
        async with session.get(url, headers=headers, ssl=ssl) as resp:
            resp.raise_for_status()
            data = await resp.json()

    return data
