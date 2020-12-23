import collections
from typing import List

from pyphorus import Device


def strip_duplicate_ips(devices: List[Device]) -> List[Device]:
    """
    Group by the device ip, since many open ports could be present on a single device
    :param devices:
    :return:
    """

    seen = collections.OrderedDict()

    for obj in devices:
        # eliminate this check if you want the last item
        if obj.ip not in seen:
            seen[obj.ip] = obj

    return list(seen.values())
