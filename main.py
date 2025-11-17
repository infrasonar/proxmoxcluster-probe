from libprobe.probe import Probe
from lib.check.cluster import CheckCluster
from lib.check.ha import CheckHA
from lib.check.backup import CheckBackup
from lib.check.guests import CheckGuests
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckCluster,
        CheckHA,
        CheckBackup,
        CheckGuests,
    )

    probe = Probe("proxmoxcluster", version, checks)

    probe.start()
