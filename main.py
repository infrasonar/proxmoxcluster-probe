from libprobe.probe import Probe
from lib.check.cluster import check_cluster
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'cluster': check_cluster
    }

    probe = Probe("proxmoxcluster", version, checks)

    probe.start()
