from libprobe.probe import Probe
from lib.check.cluster import check_cluster
from lib.check.ha import check_ha
from lib.check.backup import check_backup
from lib.check.guests import check_guests
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'cluster': check_cluster,
        'ha': check_ha,
        'backup': check_backup,
        'guests': check_guests,
    }

    probe = Probe("proxmoxcluster", version, checks)

    probe.start()
