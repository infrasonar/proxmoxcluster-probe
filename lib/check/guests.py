from libprobe.asset import Asset
from libprobe.check import Check
from ..helpers import api_request


class CheckGuests(Check):
    key = 'guests'

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        uri = '/resources'
        data = await api_request(asset, local_config, config, uri)

        vm = []
        ct = []
        for item in data['data']:
            if item['type'] == 'qemu':
                vm.append({
                    'name': str(item['vmid']),  # str
                    'vmid': item['vmid'],  # int
                    'vm_name': item['name'],  # str
                    'node': item['node'],  # str
                    'status': item['status'],  # str
                    'uptime': item['uptime'],  # int
                })
            elif item['type'] == 'lxc':
                ct.append({
                    'name': str(item['vmid']),  # str
                    'vmid': item['vmid'],  # int
                    'ct_name': item['name'],  # str
                    'node': item['node'],  # str
                    'status': item['status'],  # str
                    'uptime': item['uptime'],  # int
                })

        return {
            'vm': vm,
            'ct': ct,
        }
