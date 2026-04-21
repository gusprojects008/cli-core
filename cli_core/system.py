import os
import sys

def check_root():
    if os.geteuid() != 0:
        raise PermissionError(
            f"Run as root: sudo {' '.join(sys.argv)}"
        )
