from contextlib import contextmanager
from fcntl import LOCK_EX, LOCK_SH, LOCK_UN, lockf


@contextmanager
def lock_file(file_path, mode='r', exclusive=False):
    file_object = None
    if exclusive:
        cmd = LOCK_EX
    else:
        cmd = LOCK_SH

    try:
        file_object = open(file_path, mode=mode)
        lockf(file_object, cmd)
        yield file_object
    finally:
        if file_object is not None:
            lockf(file_object, LOCK_UN)
            file_object.close()

