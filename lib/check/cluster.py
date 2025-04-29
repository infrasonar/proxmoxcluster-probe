import logging
from libprobe import logger
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
from ..helpers import api_request


async def check_cluster(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:
    uri = '/api2/json/cluster/status'
    data = await api_request(asset, asset_config, config, uri)
    try:
        cluster = {}
        nodes = []
        backups = []
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
                    'level': item['leve'],  # str
                })

        uri = '/api2/json/cluster/ha/status/manager_status'
        data = await api_request(asset, asset_config, config, uri)

        lrm_status = data['data']['lrm_status']
        node_status = data['data']['manager_status']['node_status']
        for node in nodes:
            item = lrm_status[node['name']]
            node['mode'] = item['mode']  # str
            node['state'] = item['state']  # str
            node['status'] = node_status[node['name']]  # str

        cluster['master_node'] = \
            data['data']['manager_status']['master_node']  # str

        uri = '/api2/json/cluster/backup'
        data = await api_request(asset, asset_config, config, uri)
        for item in data['data']:
            if item['type'] == 'vzdump':
                backups.append({
                    'name': item['id'],  # str
                    'type': item['type'],  # str
                    'schedule': item['schedule'],  # str
                    'next_run': item['next-run'],  # int (unix timestamp)
                    'mode': item['mode'],  # str
                    'storage': item['storage'],  # str
                    'enabled': bool(item['enabled']),  # int->bool
                })
            else:
                logging.warning(f'unsupported backup type: {item["type"]}')
    except Exception:
        logger.exception()
        raise

    return {
        'cluster': [cluster],
        'nodes': nodes,
        'backups': backups,
    }
