import os
import re
import time
import yaml

from . import logger
from . import system
from . import context
from . import mysql
from . import compress
from . import upload
from . import notify


BACKUPS_DUMPS     = os.environ.get("BACKUPS_DUMPS", "/tmp/backups")
BACKUPS_MYSQLDUMP = os.environ.get("BACKUPS_MYSQLDUMP", "mysqldump")
BACKUPS_LOGLEVEL  = os.environ.get("BACKUPS_LOGLEVEL", "INFO")
BACKUPS_STDERR    = os.environ.get("BACKUPS_STDERR", "/tmp/backups.err")


class Runner:

  context = context.Context()
  verbose = False

  def __init__(self, file, dryrun):
    system.dryrun = dryrun

    self.context.file   = file
    self.context.dryrun = dryrun
    self.context.dumps  = BACKUPS_DUMPS
    self.context.stderr = BACKUPS_STDERR

    if not os.path.isfile(self.context.file):
      raise RuntimeError(f"File '{self.context.file}' doesn't exist.")

    self.data = self.parse(self.context.file)

    if not "backups" in self.data.keys():
      raise RuntimeError(f"File '{self.file}' doesn't have a backups top key.")

    self.backups = self.data["backups"]
    if not "jobs" in self.backups.keys():
      raise RuntimeError(f"File '{self.file}' doesn't have a jobs defined.")


  def load(self, job):
    if not job in self.backups["jobs"].keys():
      raise RuntimeError(f"Backup job '{job}' doesn't exist.")

    self.context.job = job

    self.backup  = self.backups["jobs"][job]
    self.options = self.backup.get("options", {})


  def dump(self):
    print(yaml.dump(self.data, sort_keys=False))


  def ls(self):
    for job in self.backups["jobs"]:
      print(job)


  def show(self, job):
    self.load(job)
    print(yaml.dump(self.backup, sort_keys=False))


  def databases(self, job):
    self.load(job)

    self.mysql = mysql.Mysql(self.backup["connection"])
    rows = self.mysql.query("SHOW DATABASES")
    for i in rows:
      print(i["Database"])


  def run(self, job, database):
    system.verbose = self.verbose

    self.load(job)
    self.mysql = mysql.Mysql(self.backup["connection"])
    self.prepare(job, database)

    if database:
      self.dump_database(database)

    elif self.options.get("server", False) == True:
      self.dump_server()

    else:
      databases = self.options.get("databases", [])
      self.dump_databases(databases)

    self.compress()
    self.upload()
    self.cleanup()
    self.notify()

    report = {
      "context":  self.context
    }

    return report


  def prepare(self, job, database=None):
    date = time.strftime("%Y/%m/%d")
    now  = time.strftime("%Y-%m-%d-%H%M%S")
    name = job

    if database:
      name = job + "-" + database

    self.context.dump = f"{self.context.dumps}/{name}/{date}/{now}"

    logger.info(f"Using dir {system.green(self.context.dump)}")
    system.exec(f"mkdir -p {self.context.dump}")


  def get_mysql_dump(self):
    return "%s -alv --host=%s --user=%s --password=%s --master-data=%i --triggers --events --dump-date --debug-info --single-transaction" % \
      (
        BACKUPS_MYSQLDUMP,
        self.backup["connection"].get("host", ""),
        self.backup["connection"].get("username", ""),
        self.backup["connection"].get("password", ""),
        self.options.get("master-data", 0),
      )


  def dump_server(self):
    logger.info("Dumping the server into a single file")

    sql_file = "%s/%s%s.sql" % (self.context.dump, self.options.get("prefix", ""), "all-databases")
    err_file = self.options.get("stderr", self.context.stderr)
    command  = f"{self.get_mysql_dump()} --all-databases > {sql_file} 2>{err_file}"

    system.exec(command)



  def dump_databases(self, databases):
    logger.info("Dumping databases")

    ignore  = self.options.get("ignore", [])
    ignored = ignore + ["information_schema", "performance_schema", "sys"]

    if len(databases) < 1:
      rows = self.mysql.query("SELECT SCHEMA_NAME db FROM information_schema.SCHEMATA")
      for row in rows:
        db = row["db"]
        if db in ignored:
          logger.info(f"Ignoring {system.green(db)}")
          continue

        databases.append(db)

    for database in databases:
      self.dump_database(database)


  def dump_database(self, database):
    logger.info(f"Dumping database {system.green(database)}")

    sql_file = "%s/%s%s.sql" % (self.context.dump, self.options.get("prefix", ""), database)
    err_file = self.options.get("stderr", self.context.stderr)
    command  = f"{self.get_mysql_dump()} --databases {database} > {sql_file} 2>{err_file}"

    system.exec(command)


  def compress(self):
    methods = self.backup.get("compress", [])
    if methods is []:
      logger.info("Skipping compress")
      return

    for config in methods:
      f = getattr(compress, "compress_" + config["type"])
      f(config, self.context)


  def upload(self):
    methods = self.backup.get("upload", [])
    if methods is []:
      logger.info("Skipping uploads")
      return

    for config in methods:
      f = getattr(upload, "upload_" + config["type"])
      f(config, self.context)


  def notify(self):
    methods = self.backup.get("notify", [])
    if methods is []:
      logger.info("Skipping notify")
      return

    for config in methods:
      f = getattr(notify, "notify_" + config["type"])
      f(config, self.context)


  def cleanup(self):
    clean = self.options.get("clean", "all")
    if not clean:
      logger.info(f"Skip cleaning {system.green(self.context.dump)} (clean: {clean})")
      return

    start = os.path.dirname(self.context.dump)
    stop = self.context.dumps
    logger.info(f"Cleaning from {system.green(start)} until {system.green(stop)}")
    system.exec(f"rm -frv {self.context.dump}* >>{self.context.stderr} 2>&1")
    system.cleanup(start, stop)


  def parse(self, file):
    loader  = yaml.SafeLoader
    tagEnv  = '!Env'
    tagConf = '!Conf'

    patternEnv  = re.compile('.*?\${(\w+):?(.*)}.*?')
    patternConf = re.compile('@(.*)')

    loader.add_implicit_resolver(tagEnv,  patternEnv,  None)
    loader.add_implicit_resolver(tagConf, patternConf, None)

    def constructorEnv(loader, node):
      value = loader.construct_scalar(node)
      match = patternEnv.findall(value)
      if match:
        res = value
        for group in match:
          var = os.environ.get(group[0], group[1] or f"${group[0]}")
          res = res.replace(value, var)
        return res

      return value

    def constructorConf(loader, node):
      value = loader.construct_scalar(node)
      match = patternConf.findall(value)
      if match:
        env = {}
        with open(match[0], "r") as f:
          for line in f.readlines():
            if line.find("=") > 0:
              key, val = line.split("=")
              env[key] = val.strip()
              os.environ[key] = env[key]
          return env
      return value

    loader.add_constructor(tagEnv,  constructorEnv)
    loader.add_constructor(tagConf, constructorConf)

    with open(file, "r") as f:
      data = yaml.load(f, Loader=loader)

    return data
