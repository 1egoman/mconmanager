#!/usr/bin/env python

from optparse import OptionParser
import json, os, time, pty, urllib2
import subprocess as sp

import config_handler
import server as srvr

# main app for the McoN manager
class app(object):
  SERVERLOC = "/home/ryan/Desktop/mcd/servers"
  STARTSCRIPT = "launch.sh"

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



  def add_args(self):
    self.parser = OptionParser(usage="usage: %prog [server] [options]", version="McoN Deamon v1.0 - By Ryan Gaus")

    # action flag
    # self.parser.add_option("-a", "--action",
    #   action="store",
    #   dest="action_flag",
    #   default="status",
    #   help="action to do for the server: start,stop,restart,attach,status,addserver,prop")

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


    # install plugin flag
    self.parser.add_option("", "--install",
      action="store",
      dest="instplugin_flag",
      default=False,
      help="install plugin specified on server")



  def __init__(self):
    # load in the json for config file
    self.json = config_handler.load_json()
    self.config = self.json.read()

    # add arguments for the script's parser
    self.add_args()

    # parse the args, turn options into a dict
    (options, args) = self.parser.parse_args()
    options = vars(options)


    # print "OUT", options, args

    # add server
    if options.has_key("addserver_flag") and options["addserver_flag"]: srvr.add_server()

    # server is good...
    if args and (args[0].rstrip("/") in self.config["server-list"] or args[0].rstrip("/") == "all") and len(args) != 0:
      # server exists
      self.provide_output(args[0].rstrip("/"), options, args)

    else:
      self.parser.error("Server Doesn't Exist, or wasn't specified.")


if __name__ == '__main__':
  app()