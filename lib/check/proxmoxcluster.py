import aiohttp
from libprobe.asset import Asset
from libprobe.exceptions import CheckException


DEFAULT_PORT = 8006


async def check_proxmoxcluster(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:
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
    url = f'{base_url}/api2/json/cluster/resources'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=ssl) as resp:
            resp.raise_for_status()
            data = await resp.json()

    guests = [{
        'name': str(n['vmid']),  # str
        'node': n.get('node'),  # str
        'status': n.get('status'),  # str
        'vm_name': n.get('name'),  # str
    } for n in data['data'] if n['type'] == 'qemu']
    nodes = [{
        'name': n['node'],  # str
        'cgroup_mode': n.get('cgroup-mode'),  # int
        'id': n.get('id'),  # str
        'level': n.get('level'),  # str
        'status': n.get('status'),  # str
    } for n in data['data'] if n['type'] == 'node']
    return {
        'guests': guests,
        'nodes': nodes,
    }
