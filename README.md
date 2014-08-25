MCONMANAGER...
============================

...is a tool for managing multiple minecraft servers on a machine with GNU's SCREEN command for *NIX systems. 

###Why McoNManager?
I used to run a minecraft server network known as the MineCraft Open Network and I needed a program to help me manage it. 

###Help Menu

Usage: main.py [server] [options]
 
* Options:
*   --version             show program's version number and exit
*   -h, --help            show this help message and exit
*   -t, --start           start server
*   -p, --stop            stop server
*   -r, --restart         restart server
*   -a, --attach          attach server
*   -s, --status          status of server
*   -n, --newserver       add new server
*   -e, --properties      show server.properties
*   --reset               reset/create config file
*   --import=SERVERNAME   import server into config file

###Getting Started
1. Clone the repository
2. Run the mcon.sh file, with an argument of --reset
3. Wait for the program to complete
4. Done! You probably want to create or import a server next.

###Modules Required (For Python)
**NOTE: All modules should exsist in a fresh install of python. I have developed against 2.7.x**
* json
* time
* subprocess
* urllib2
* optparse
* shutil

*Please note McoNManager is no longer used, and can basically be considered abandoned*
