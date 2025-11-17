import logging
from libprobe.asset import Asset
from libprobe.check import Check
from ..helpers import api_request


class CheckBackup(Check):
    key = 'backup'

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        uri = '/backup'
        data = await api_request(asset, local_config, config, uri)

        backups = []
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
