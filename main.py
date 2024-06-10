from libprobe.probe import Probe
from lib.check.proxmoxcluster import check_proxmoxcluster
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'proxmoxcluster': check_proxmoxcluster
    }

    probe = Probe("proxmoxcluster", version, checks)

    probe.start()
