import re
import datetime
from collections import defaultdict


def group_by_filenames(filenames, limit=5):
    d = defaultdict(list)
    ret = []

    for filename in filenames:
        match = re.match(r'^(.+)\.(\d+)ms\.(\d+)\.prof', filename)
        if not match:
            continue
        try:
            func, ms, timestamp = match.group(1), match.group(2), match.group(3)
        except IndexError:
            continue
        d[func].append([filename, ms, datetime.datetime.fromtimestamp(float(timestamp))])

    for func, l in d.iteritems():
        l.sort(key=lambda x: x[1])

        if limit and len(l) > limit:
            l = l[::len(l)/limit]
        ret.append((func, l))
    return ret
