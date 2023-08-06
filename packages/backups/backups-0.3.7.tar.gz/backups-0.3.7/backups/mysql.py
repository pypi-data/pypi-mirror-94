import MySQLdb


class Mysql:

  def __init__(self, config):
    self.config = config

    args = {
      "host":   self.config["host"],
      "user":   self.config["username"],
      "passwd": self.config["password"],
    }

    if self.config.get("database") is not None:
      args["db"] = self.config["database"]

    self.connection = MySQLdb.connect(**args)


  def query(self, sql, params={}):
    cursor = self.connection.cursor()
    cursor.execute(sql, params)
    cols = [col[0] for col in cursor.description]
    rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
    cursor.close()

    return rows
