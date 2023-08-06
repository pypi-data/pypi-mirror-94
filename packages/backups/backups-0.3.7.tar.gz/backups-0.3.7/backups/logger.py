import time
import logging

# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(
#   level=logging.INFO,
#   format="%(asctime)s  %(message)s"
# )

# logger = logging.Logger()
logger = logging.getLogger("backups")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

def info(message):
  now = time.strftime("%Y-%m-%d %H:%M:%S")
  logger.info("\033[38;5;242m%s\033[0m  %s" %(now, message))


def debug(message):
  # print(message)
  pass
