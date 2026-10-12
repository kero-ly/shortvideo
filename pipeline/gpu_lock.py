"""Cross-process admission lock for this factory, not for other server users."""
import fcntl
from pathlib import Path

def acquire(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle=path.open('a+')
    try:
        fcntl.flock(handle.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close()
        raise RuntimeError('Another factory GPU job is already running') from None
    return handle
