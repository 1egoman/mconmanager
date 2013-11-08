#!/usr/bin/env python

from optparse import OptionParser
import json, os, time, urllib2
import subprocess as sp

import config_handler
import server as srvr

# main app for the McoN manager
class app(object):
  SERVERLOC = "/home/ryan/Desktop/mcd/servers"
  STARTSCRIPT = "launch.sh"

  DEFAULTCONFIGLINES = """

{
  "ads": [],
  "plugin-dict": {
    "essentials": "http://dev.bukkit.org/media/files/748/504/Essentials.zip",
    "pex": "http://dev.bukkit.org/media/files/742/103/PermissionsEx.jar",
    "worldedit": "http://dev.bukkit.org/media/files/739/932/worldedit-5.5.8.zip"
  },
  "server-list": {},
  "server-location": "%LOCATION",
  "server-startscript-name": "launch.sh",
  "server-types": {
    "bukkit": {
      "defaults": {
        "display-ads": true,
        "seed": false,
        "type": "bukkit",
        "version": "1.6.4",
        "default-plugins": []
      },
      "is-vanilla": false,
      "location": "http://cbukk.it/latest-rb/craftbukkit.jar",
      "use-plugins": true
    },
    "spigot": {
      "defaults": {
        "display-ads": true,
        "seed": false,
        "type": "spigot",
        "version": "1.6.4",
        "default-plugins": []
      },
      "is-vanilla": false,
      "location": "http://ci.md-5.net/job/Spigot/lastBuild/artifact/Spigot-Server/target/spigot.jar",
      "use-plugins": true
    },
    "vanilla": {
      "defaults": {
        "display-ads": true,
        "seed": false,
        "type": "vanilla",
        "version": "1.7.2"
      },
      "is-vanilla": true,
      "location": "https://s3.amazonaws.com/Minecraft.Download/versions/%VERSION/minecraft_server.%VERSION.jar",
      "use-plugins": false
    }
  }
}
"""

  def provide_output(self, server, options, args):
    
    # create a new 'server'
    sc = srvr.server(server)

    if options.has_key("start_flag") and options["start_flag"]:
      print "Starting Server(s)... "
      if sc.start_server(): 
        print "Done"

    elif options.has_key("stop_flag") and options["stop_flag"]:
      print "Stopping Server(s)... "
      if sc.stop_server(): 
        print "Done"

    elif options.has_key("restart_flag") and options["restart_flag"]:
      print "Restarting Server... "
      a = sc.restart_server()
      print "Done"



    elif options.has_key("prop_flag") and options["prop_flag"] and server != "all": sc.open_prop()
    elif options.has_key("attach_flag") and options["attach_flag"]: sc.attach()
  # elif options.has_key("instplugin_flag") and options["instplugin_flag"]: sc.install_plugin( options["instplugin_flag"] )

    elif server == "all":
      for svr in self.config["server-list"].keys():
        print "'"+svr+"'", sc.server_on(svr)
      
    elif server:
      print "'"+server+"'"
      online = sc.server_on(server)
      s = self.config['server-list'][server]
      print "Online:", online
      print "Type:", s['type']
      print "Version:", s['version']


  def reset_config(self):

    # see if a config file already exists
    if os.path.exists("config.json"):
      ans = raw_input("A config file already exists. It will be backed up as config.bkp.json. Continue? (y or n)").lower()
      if not (ans == "y" or ans == "yes"): return False
      try:
        import shutil
        shutil.copy("config.json", "config.bkp.json")

      # eg. src and dest are the same file
      except shutil.Error as e:
          print 'Error: %s' % e
          return False

      # eg. source or destination doesn't exist
      except IOError as e:
          print 'Error: %s' % e.strerror
          return False

    # reset config file for default
    print "Creating config.json..."

    # get server location
    loc = raw_input("Where to put server files (server's location): ")
    if not os.path.exists(loc): os.mkdir(loc)

    with open("config.json", "w") as f:
      f.write( self.DEFAULTCONFIGLINES.replace("%LOCATION", loc) )
    print "Done!"



  def add_args(self):
    self.parser = OptionParser(usage="usage: %prog [server] [options]", version="McoN Deamon v1.0 - By Ryan Gaus (rgaus.net)")

    # start flag
    self.parser.add_option("-t", "--start",
      action="store_true",
      dest="start_flag",
      default=False,
      help="start server")

    # stop flag
    self.parser.add_option("-p", "--stop",
      action="store_true",
      dest="stop_flag",
      default=False,
      help="stop server")

    # restart flag
    self.parser.add_option("-r", "--restart",
      action="store_true",
      dest="restart_flag",
      default=False,
      help="restart server")

    # attach flag
    self.parser.add_option("-a", "--attach",
      action="store_true",
      dest="attach_flag",
      default=False,
      help="attach server")

    # status flag
    self.parser.add_option("-s", "--status",
      action="store_true",
      dest="status_flag",
      default=False,
      help="status of server")

    # addserver flag
    self.parser.add_option("-n", "--newserver",
      action="store_true",
      dest="addserver_flag",
      default=False,
      help="add new server")

    # prop flag
    self.parser.add_option("-e", "--properties",
      action="store_true",
      dest="prop_flag",
      default=False,
      help="show server.properties")


    # reset flag
    self.parser.add_option("", "--reset",
      action="store_true",
      dest="configure_flag",
      default=False,
      help="reset/create config file")

    # import flag
    self.parser.add_option("", "--import",
      action="store",
      dest="import_flag",
      default=False,
      help="import server into config file")



  def __init__(self):

    # add arguments for the script's parser
    self.add_args()

    # parse the args, turn options into a dict
    (options, args) = self.parser.parse_args()
    options = vars(options)

    # reset config file
    if options.has_key("configure_flag") and options["configure_flag"]: 
      self.reset_config()
      return

    # import a server
    elif options.has_key("import_flag") and options["import_flag"]: 
      srvr.import_server( options["import_flag"] )
      return


    # load in the json for config file
    self.json = config_handler.load_json()
    self.config = self.json.read()



    # add server
    if options.has_key("addserver_flag") and options["addserver_flag"]: srvr.add_server()

    # server is good...
    elif args and (args[0].rstrip("/") in self.config["server-list"] or args[0].rstrip("/") == "all") and len(args) != 0:
      # server exists
      self.provide_output(args[0].rstrip("/"), options, args)

    else:
      # server not good
      self.parser.error("Server Doesn't Exist, or wasn't specified.")


if __name__ == '__main__':
  app()