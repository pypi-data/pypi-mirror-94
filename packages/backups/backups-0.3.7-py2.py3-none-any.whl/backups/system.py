import os

from . import logger

dryrun  = False
verbose = False

def exec(command):
  if verbose:
    logger.info(f"\033[38;5;242mRunning '{command}'\033[0m")

  if dryrun:
    return

  code = os.system(command)
  if code != 0:
    raise RuntimeError(f"Command '\033[31;1m{command}\033[0m' failed.")


def size(bytes, suffix="B"):
  for unit in ["","K","M","G","T","P","E","Z"]:
    if abs(bytes) < 1024.0:
      return "%3.1f %s%s" % (bytes, unit, suffix)
    bytes /= 1024.0

  return "%.1f %s%s" % (bytes, "Y", suffix)


def green(text):
  return f"\033[32;1m{text}\033[0m"


def cleanup(start, stop):
  while start != stop:
    try:
      exec(f"rmdir {start}")
    except Exception as e:
      print(f"Failed to remove dir {start}")
      return

    start = os.path.dirname(start)
