import json
import requests


def _size(context):
  if context.compress is []:
    return "-"

  size = ""
  for compression in context.compress:
    size = f"{size}{compression['size']['human']}, "

  size = f"{size[0:-2]}"
  return size


def notify_slack(config, context):
  webhook = config.get("webhook")
  text    = f"Backup `{context.job}` completed with *{_size(context)}*"
  channel = config.get("channel", "#backups")

  payload = {
    "text": text,
    "channel": channel,
  }

  res = requests.post(webhook,
    data=json.dumps(payload),
    headers={'Content-Type': 'application/json'}
  )

  if res.status_code != 200:
    raise RuntimeError(
      'Request to slack returned an error %s, the response is:\n%s'
      % (res.status_code, res.text)
    )

  context.notify.append({
    "type": "slack",
    "text": text,
    "status": res.status_code,
    "channel": channel,
  })
