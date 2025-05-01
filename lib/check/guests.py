from libprobe.asset import Asset
from ..helpers import api_request


async def check_guests(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:

    uri = '/resources'
    data = await api_request(asset, asset_config, config, uri)

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
