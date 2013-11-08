import subprocess as sp
import json, os, time, urllib2
import config_handler

class server(object):
  # represents a server to be interfaced with

  def __init__(self, name):
    self.name = name

    # read in config file
    self.json = config_handler.load_json()
    self.config = self.json.read()

    self.SERVERLOC = self.config['server-location']
    self.STARTSCRIPT = self.config['server-startscript-name']



  def cmd(self, cmd):
    # run command on server
    if self.server_on(self.name):
      return self.c(["screen", "-p", "0", "-S", "mc-"+self.name, "-X", "stuff", cmd+"\n"])
    else:
      return False



  def c(self, *args):
    # run a (unix) command
    s = sp.Popen(*args, stderr=sp.STDOUT, stdout=sp.PIPE).communicate()[0]
    return s


  def open_prop(self, editor="nano"):
    sp.call([editor, os.path.join(self.SERVERLOC, self.name, "server.properties")])



  def attach(self):
    # attach to screen session
    if self.server_on(self.name):
      sp.call(["screen", "-x", "mc-"+self.name])



  def server_on(self, s):
    # is server on?
    self.c(["screen", "-wipe"]) # clear out any dead screens
    return "mc-"+s in str( self.c(["screen", "-ls"]) )


  def install_plugin(self, p):
    if not self.config["server-types"][ self.config["server-list"][self.name]["type"] ]["use-plugins"]:
      print "Cannot intall plugins."
      return False


    # get and install plugin
    for pl in p.split(" "):

      if self.config["plugin-dict"].has_key(pl): 
        url = self.config["plugin-dict"][pl]
        # download plugin
        sp.call(["wget", "-O", os.path.join(config["server-location"], self.name, "plugins", pl+".jar"), url])

      else:
        print "unknown plugin", pl
        return False



  def start_server(self):
    # start server

    if self.name == "all":
      # turn on all servers
      for svr in self.config["server-list"].keys():
        print "Starting", svr
        if not self.server_on(svr):
          os.chdir( os.path.join(self.SERVERLOC, svr) )
          self.c(["sh", self.STARTSCRIPT])

    elif not self.server_on(self.name):
      os.chdir( os.path.join(self.SERVERLOC, self.name) )
      self.c(["sh", self.STARTSCRIPT])
      return True

    else:
      print "Server already on."
      return False


  def restart_server(self):
    # restart server
    self.stop_server()
    time.sleep(1)
    self.start_server()



  def stop_server(self):
    # stop server 's'

    if self.name == "all":
      # turn off all servers

      for svr in self.config["server-list"].keys():
        print "Stopping", svr
        # if server is on...
        if self.server_on(svr):
          # stop it
          os.chdir( os.path.join(self.SERVERLOC, svr) )
          return self.c(["screen", "-p", "0", "-S", "mc-"+self.name, "-X", "stuff", "stop\n"])

      return True

    elif self.server_on(self.name):
      os.chdir( os.path.join(self.SERVERLOC, self.name) )
      if self.cmd("stop") != False: return True

    else:
      print "Server already on."
      return False


def import_server(s):
  # open json file
  fjson = config_handler.load_json()
  config = fjson.read()

  # see if s is a valid server name
  if "/" in s or "\\" in s: 
    print "Don't specify a path, pick a server already in your server folder!"
    return False

  else:

    # print all server types, pick one for the new server
    stype = ""
    while not stype.isdigit():
      c = 0
      for i in config["server-types"].keys():
        print str(c)+".", i
        c += 1
      stype = raw_input("server type (ex. 1)> ")

    # get server info
    server_info = config["server-types"][ config["server-types"].keys()[int(stype)] ]

    # add to json config file
    config["server-list"][s] = server_info["defaults"]
    fjson.write(config)
    print "Done!"

def add_server():
  # open json config file
  fjson = config_handler.load_json()
  config = fjson.read()

  print "New Server:"

  # input the name
  name = raw_input("name> ")
  if name == "all": return

  # print all server types, pick one
  stype = ""
  while not stype.isdigit():
    c = 0
    for i in config["server-types"].keys():
      print str(c)+".", i
      c += 1
    stype = raw_input("server type (ex. 1)> ")

  # get server info
  server_info = config["server-types"][ config["server-types"].keys()[int(stype)] ]

  # input other info
  port = raw_input("port> ")
  ram = raw_input("ram (ex 1G or 512MB)> ")


  # START MAKING SERVER


  # make server dir
  if not os.path.exists(os.path.join(config["server-location"], name)): 
    os.mkdir( os.path.join(config["server-location"], name) )
    print os.path.join(config["server-location"], name)

  # get server jar
  # print server_info
  url = server_info["location"].replace("%VERSION", server_info['defaults']['version'])
  sp.call(["wget", "-O", os.path.join(config["server-location"], name, "minecraft.jar"), url])
  # chmod it
  sp.call(["chmod", "775", os.path.join(config["server-location"], name, "minecraft.jar")])
  print "Downloaded Server JAR"

  # write server.properties
  with file(os.path.join(config["server-location"], name, "server.properties"), "w") as f:
    f.write("server-port="+port)
  print "Wrote server.properties"

  # and launch script
  with file(os.path.join(config["server-location"], name, config["server-startscript-name"]), "w") as f:
    f.write("#!/bin/bash\n")
    f.write("screen -dmS mc-"+name+" java -Xmx"+ram+" -Xms"+ram+" -jar minecraft.jar nogui\n")

  # chmod the script
  sp.call(["chmod", "775", os.path.join(config["server-location"], name, config["server-startscript-name"])])
  print "Wrote Launch script"

  # lastly, add to json config file
  config["server-list"][name] = server_info["defaults"]
  fjson.write(config)
  print "Wrote JSON config file"

  # done!
  print "Made Server!"