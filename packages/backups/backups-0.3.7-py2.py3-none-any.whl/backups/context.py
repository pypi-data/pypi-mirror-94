from . import data

class Context(data.Object):

  def __init__(self):
    self.file   = None
    self.job    = None
    self.dumps  = None
    self.dump   = None
    self.stderr = None
    self.dryrun = None

    self.compress = []
    self.upload   = []
    self.notify   = []
