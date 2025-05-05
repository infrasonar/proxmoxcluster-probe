import logging
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
from ..helpers import api_request


async def check_ha(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:

    uri = '/ha/status/manager_status'
    data = await api_request(asset, asset_config, config, uri)

    try:
        lrm_status = data['data']['lrm_status']
        node_status = data['data']['manager_status']['node_status']
    except Exception:
        raise CheckException(
            'Failed to read High Availability (HA) status. This check '
            'requires HA to be enabled on the cluster. Either ensure '
            'high availability is configured and running, or disable '
            'the `ha` check.')

    nodes = []
    for name, item in lrm_status.items():
        nodes.append({
            'name': name,
            'mode': item['mode'],  # str
            'state': item['state'],  # str
            'status': node_status[name],  # str
        })

    ha = {
        'name': 'ha',
        'master_node': data['data']['manager_status']['master_node']  # str
    }

    return {
        'ha': [ha],
        'nodes': nodes,
    }
