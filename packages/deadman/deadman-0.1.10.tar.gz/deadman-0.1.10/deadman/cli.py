import os
import sys
import yaml
import requests
import collections

# Default alert structure
defaults = {
  "url": "required",
  "auth": None,
  "slack": {
    "webhook": None,
  },
  "status": {
    "ok": [200, 201, 202, 204],
  }
}

COLORS = {
  "red"     : "31;1",
  "green"   : "32;1",
  "yellow"  : "33;1",
  "blue"    : "34;1",
}


def merge(dest, defaults):
  """
  Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
  updating only top-level keys, dict_merge recurses down into dicts nested
  to an arbitrary depth, updating keys. The ``source`` is merged into `dest`.
  Copied from https://gist.github.com/angstwad/bf22d1822c38a92ec0a9

  :param dest: dict onto which the merge is executed
  :param defaults: The defaults
  :return: None
  """
  for k, v in defaults.items():
    if (k in dest and isinstance(dest[k], dict)
      and isinstance(v, collections.abc.Mapping)):
      merge(dest[k], v)
    else:
      dest[k] = v


def paint(color, text):
  code = COLORS.get(color, "32;1")
  print(f"\033[{code}m==> {text}\033[0m")


def check(alert):
  url = alert["url"]

  try:
    res = requests.get(url)
    oks = alert["status"]["ok"]
    msg = f"Url *{url}* returned a `{res.status_code}` status."

    if res.status_code in oks:
      paint("green", f"PASS {msg}")
      return

    paint("red", f"FAIL {msg}")
    notify(alert["slack"], msg)

  except Exception as ex:
    paint("red", f"EXCEPTION {ex}")
    notify(alert["slack"], f"*Error on {url}*: `{type(e)}`\n\n> {e}")


def notify(slack, message):
  channel  = slack.get("channel", "#general")
  emoji    = slack.get("emoji", ":robot_face:")
  username = slack.get("user", "Deadman")

  payload = {
    "text": message,
    "channel": channel,
    "username": username,
    "icon_emoji": emoji,
  }

  try:
    res = requests.post(slack["webhook"], json=payload)
    paint("green", f"Slack sent with code {res.status_code} to channel {channel}")

  except Exception as ex:
    paint("red", f"EXCEPTION {ex}")


def main():
  file = os.environ.get("DEADMAN_FILE", "alerts.yaml")
  if len(sys.argv) > 1:
    file = sys.argv[1]

  data = yaml.safe_load(open(file, "r"))
  merge(defaults, data.get("defaults", {}))
  alerts = data.get("alerts", [])
  for alert in alerts:
    merged = defaults
    merge(merged, alert)
    check(merged)


if __name__ == "__main__":
  main()
