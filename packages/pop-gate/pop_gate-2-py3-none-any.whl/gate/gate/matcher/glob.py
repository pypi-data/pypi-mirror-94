# Import python libs
import fnmatch
from typing import List


def match(hub, ref: str, prefix: str, refs: List[str]) -> bool:
    """
    Check the desired ref to see if it matches a globular ref in the refs list
    """
    for pattern in refs:
        if prefix:
            pattern = f"{prefix}.{pattern}"
        if fnmatch.fnmatch(ref, pattern):
            return True
    else:
        return False
