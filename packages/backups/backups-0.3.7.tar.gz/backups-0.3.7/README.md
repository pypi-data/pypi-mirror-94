# Backups

[![Github Status](https://github.com/ptdorf/backups/workflows/.github/workflows/test.yaml/badge.svg)](https://github.com/ptdorf/backups/actions)
<!--
[![Travis Status](https://travis-ci.org/ptdorf/backups.svg?branch=master)](https://travis-ci.org/ptdorf/backups)
-->

Tool to backup databases.


## Installation

    pip install --upgrade backups


## Usage

```
$ backups --help
Backups mysql databases

Usage:
  backups env
  backups ls                    [--file FILE] [--verbose]
  backups show JOB              [--file FILE] [--verbose]
  backups databases JOB         [--file FILE] [--verbose]
  backups run JOB               [--file FILE] [--verbose] [--dryrun]
  backups run JOB [DATABASE]    [--file FILE] [--verbose] [--dryrun]

Commands:
  env         Show the current environment
  ls          Prints the backup job names
  show        Prints the configuration for a job
  databases   Lists all databases on a backup job server
  run         Runs the backup for a job

Options:
  -f --file FILE    The backups config file (default /etc/backups/backups.yaml)
  -d --dryrun       Just prints the commands but doesn't execute them
  -v --verbose      Adds verbosity
  -h --help         Prints this help
     --version      Prints the current version

Environment variables:
  BACKUPS_FILE          The backups file (default /etc/backups/backups.yaml)
  BACKUPS_DUMPS_DIR     The dumps directory (default /tmp/backups)
  BACKUPS_MYSQLDUMP     The mysqldump binary (default picked from $PATH)
  BACKUPS_LOG_LEVEL     Default INFO
  BACKUPS_STDERR        The stderr log file (default /tmp/backups.err)

Check https://github.com/ptdorf/backups#backups for more info
```


## Setup

Create a `backups.yaml` file with content similar to:

```yaml
backups:
  jobs:
    acme:
      connection:
        type:     mysql
        host:     !Env ${BACKUPS_DB_HOST:acme.com}
        username: !Env ${BACKUPS_DB_USERNAME:backup}
        password: !Env ${BACKUPS_DB_PASSWORD}
      options:
        # Dumps the entire server into a single file (this is the default)
        server: true
        # By default it will create a single dump file for each database found
        # Uncomment to only backups specific databases (one on each file)
        # databases:
        # - main_db
        # - other_db
      compress:
      - type:     zip
        pasword:  !Env ${BACKUPS_ZIP_PASSWORD}
      upload:
      - type:     s3
        bucket:   acme-backups
        prefix:   databases
        enabled:  true
      notify:
      - type:     slack
        channel:  "#backups"
        webhook:  !Env ${BACKUPS_SLACK_WEBHOOK:https://hooks.slack.com/services/x/y/z}
```

Notice the use of the environment variables, like `BACKUPS_DB_HOST`, used in
combination with the `!Env` yaml resolver. If they exist they get resolved to
their values. Use the format `${VAR_NAME:default_value}` to use `default_value`
if `$VAR_NAME` is not defined.

Now run it with

    backups run acme --file backups.yaml

You can use the `BACKUPS_FILE` env var instead:

    export BACKUPS_FILE=backups.yaml
    backups run acme
