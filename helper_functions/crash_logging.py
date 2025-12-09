import globals as g
import os
import datetime


def create_crash_directory():
    if not os.path.exists(g.CRASH_DIRECTORY):
        os.makedirs(g.CRASH_DIRECTORY)


def dump_request_queue():
    if len(g.request_queue) == 0:
        return

    dt = str(datetime.datetime.now().timestamp())
    if not os.path.exists(g.CRASH_DIRECTORY):
        os.makedirs(g.CRASH_DIRECTORY)

    filename = os.path.join(g.CRASH_DIRECTORY, g.CRASH_FILENAME_PREFIX + "-" + dt)

    try:
        f = open(filename, "w")
        for req in g.request_queue:
            if isinstance(req, bytearray) or isinstance(req, bytes):
                f.write(req.hex() + "\n")
            else:
                f.write(str(req) + "\n")
        f.close()
        print("Logged request queue to %s" % filename)
    except Exception as e:
        print(f"Failed to write crash log: {e}")
