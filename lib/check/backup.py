import logging
from libprobe.asset import Asset
from ..helpers import api_request


async def check_backup(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:
    backups = []

    uri = '/backup'
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

    return {
        'backups': backups,
    }
