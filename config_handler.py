import json, os

class load_json(object):
  
  def __init__(self):
    # if file doesn't exsist, make it
    if not os.path.exists("config.json"):
      f = file("servers.json", "w")
      f.write("{}")
      f.close()

    with file("servers.json", "r") as f:
      self.contents = json.loads(f.read())

  def read(self):
    with file("config.json", "r") as f:
      return json.loads(f.read())

  def write(self, w):
    with file("config.json", "w") as f:
      w = json.dumps(w, sort_keys=True, indent=2, separators=(',', ': '))
      f.write(w+"\n")
      return True