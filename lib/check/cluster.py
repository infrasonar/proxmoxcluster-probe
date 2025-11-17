from libprobe.asset import Asset
from libprobe.check import Check
from ..helpers import api_request


class CheckCluster(Check):
    key = 'cluster'

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        uri = '/status'
        data = await api_request(asset, local_config, config, uri)

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
