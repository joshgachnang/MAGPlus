#!/usr/bin/python2
import sys # import sys for getting arguments

from mag import MinecraftAssetsGetter

if __name__ == '__main__':
    mag = MinecraftAssetsGetter()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "latest":

            ######################################## print latest version
            print mag.getWeeklyList().pop()
            ########################################
    
        elif sys.argv[1] == "list":  # first argument
            if len(sys.argv) > 1:
                if sys.argv[2] == "minecraft":
    
                    ######################################## list all Minecraft entries
                    for version in mag.getMinecraftList(): 
                        print version
                    ########################################
    
                elif sys.argv[2] == "weekly":
    
                    ######################################## list all Minecraft entries
                    for version in mag.getWeeklyList(): 
                        print version
                    ########################################
    
                else:
                    print "Sry! unknown list"
            else:
    
                ######################################## list all Minecraft entries
                for version in mag.getVersionList(): 
                    print version
                ########################################
    
        elif sys.argv[1] == "client" or sys.argv[1] == "server":
            if len(sys.argv) > 1:
                if sys.argv[2] == "latest":
                    if sys.argv[1] == "client":
                        ####################################
                        print mag.getClientUrl(mag.getWeeklyList().pop())
                        ####################################

                    elif sys.argv[1] == "server":

                        ####################################
                        print mag.getServerUrl(mag.getWeeklyList().pop())
                        ####################################
                else:
                    version = sys.argv[2]
                    if version in mag.getVersionList():
                        if sys.argv[1] == "client":

                            ################################
                            print mag.getClientUrl(version)
                            ################################

                        elif sys.argv[1] == "server":

                            ################################
                            print mag.getServerUrl(version)
                            ################################

            else:
                print "call1:   ./demo.py " + sys.argv[1] + " latest"
                print "call2:   ./demo.py " + sys.argv[1] + " version 12w24a"

    else:
        print "MinecraftAssetsGetter -> mag"
        print "call4:   ./demo.py latest"
        print "call1:   ./demo.py list"
        print "call2:   ./demo.py list weekly"
        print "call3:   ./demo.py list minecraft"
        print "call5:   ./demo.py client latest"
        print "call6:   ./demo.py server version 12w24a"