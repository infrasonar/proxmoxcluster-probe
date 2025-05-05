import logging
from libprobe.asset import Asset
from ..helpers import api_request


async def check_cluster(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:
    uri = '/status'
    data = await api_request(asset, asset_config, config, uri)

    cluster = {}
    nodes = []
    for item in data['data']:
        if item['type'] == 'cluster':
            cluster['name'] = item['name']  # str
            cluster['nodes'] = item['nodes']  # int
            cluster['version'] = item['version']  # int
            cluster['quorate'] = item['quorate']  # int
            cluster['id'] = item['id']  # str
        elif item['type'] == 'node':
            nodes.append({
                'name': item['name'],  # str
                'id': item['id'],  # str
                'ip': item['ip'],  # str
                'level': item['level'],  # str
                'online': bool(item['online']),  # bool
            })

    return {
        'cluster': [cluster],
        'nodes': nodes,
    }
