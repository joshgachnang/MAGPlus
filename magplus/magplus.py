#!/usr/bin/env python
#
# MinecraftAssetsGetter -> mag0.1
#

DEBUG = False

import urllib2
import re
from datetime import datetime
from xml.dom.minidom import parseString


class MinecraftAssetsGetter:
    # last backslash in fileUrl is important
    def __init__(self, xmlUrl='http://assets.minecraft.net/', fileUrl='http://assets.minecraft.net/'):
        self.fileUrl = fileUrl
        file = urllib2.urlopen(xmlUrl)
        data = file.read()
        file.close()
        self.dom = parseString(data)

    def getVanillaVersionList(self, stable=False):
        """Returns a list of versions, sorted by date, from earliest to
        latest. versions[-1] would be the latest version.
        stable: Determines whether only stable releases are returned or not.
        """
        contents = self.dom.getElementsByTagName("Contents")
        dt = datetime.now()
        #version_list = list()
        self.date_list = {}
        for content in contents:
            key = getText(content.getElementsByTagName("Key")[0].childNodes)
            date = getText(content.getElementsByTagName("LastModified")[0].childNodes)
            try:
                version, file = key.split('/')
                if len(file) == 0:
                    #print key, ", ", key.split('/'), ', ', version
                    continue
            except ValueError:
                if DEBUG:
                    print "skip	-> " + version
            if file == "minecraft.jar" or file == "minecraft_server.jar":
                #version_list.append(version)
                if stable:
                    # Regex: 2 digits, 'w', 2 digits, 1 letter
                    if "pre" in version or "rc" in version or re.search("^\d{2}w\d{2}[a-zA-Z]{1}$", version):
                        continue
                self.date_list[date] = version
                if DEBUG:
                    print "add	-> " + version
            else:
                if DEBUG:
                    print "skip 	-> " + version
        #self.sorted_list = self.date_list.sort()
        if DEBUG:
            print self.date_list
        sorted_list = list()
        for key in sorted(self.date_list.iterkeys()):
            #print "%s: %s" % (key, self.date_list[key])
            sorted_list.append(self.date_list[key])
        #print "SET: ", set(sorted_list)
        # Filter duplicates
        return list(set(sorted_list))

    def getLatestVanillaServer(self, stable=False):
        """ Returns the URL of the latest server version.
        table: Determines whether only stable releases are returned or not.
        """
        version_list = self.getVanillaVersionList(stable)
        return self.getVanillaServerUrl(version_list[-1])

    def getLatestClient(self, stable=False):
        """ Returns the URL of the latest client version.
        table: Determines whether only stable releases are returned or not.
        """
        version_list = self.getVanillaVersionList(stable)
        return self.getClientUrl(version_list[-1])

    def getVanillaServer(self, stable=False, versions_old=0):
        """ Returns the URL of the latest server version.
        table: Determines whether only stable releases are returned or not.
        Returns None if too versions old is more than available servers.
        """
        version_list = self.getVanillaVersionList(stable)
        #print len(version_list), ', ', version_list
        if versions_old + 1 > len(version_list):
            return None
        return self.getVanillaServerUrl(version_list[-1 - versions_old])

    def getClient(self, stable=False, versions_old=0):
        """ Returns the URL of the latest client version.
        table: Determines whether only stable releases are returned or not.
        Returns None if too versions old is more than available servers.
        """
        version_list = self.getVanillaVersionList(stable)
        if versions_old + 1 > len(version_list):
            return None
        return self.getClientUrl(version_list[-1 - versions_old])

    def getVanillaServerUrl(self, version):
        """ Returns the URL of a given server version. """
        return unicode(self.fileUrl) + version + unicode("/minecraft_server.jar")

    def getClientUrl(self, version):
        """ Returns the URL of a given client version. """
        return unicode(self.fileUrl) + str(version) + unicode("/minecraft.jar")

    def getVanillaWeeklyList(self):
        return filterVersionList(self.getVanillaVersionList(), re.compile(r"\d{2}w\d{2}\w"))

    def getVanillaMinecraftList(self):
        allVersions = self.getVanillaVersionList()
        weekly = self.getWeeklyList()
        return [x for x in allVersions if x not in weekly]


def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


def filterVersionList(vlist, pattern):
    """call: filterVersionList( VersionList, re.comiple(r"\d{2}w\d{2}\w" )"""
    return_list = [x for x in vlist if not pattern.match(x) is None]
    if DEBUG:
        for version in return_list:
            print version
    return return_list

if __name__ == '__main__':
    mag = MinecraftAssetsGetter()
    #for version in mag.getVanillaVersionList():
        #print version
    print "Latest Prerelease Server: ", mag.getLatestVanillaServer()
    print "Latest Prerelease Client: ", mag.getLatestClient()
    print "Latest Stable Server: ", mag.getLatestVanillaServer(stable=True)
    print "Latest Stable Client: ", mag.getLatestClient(stable=True)
    print "Previous Prerelease Server: ", mag.getVanillaServer(versions_old=1)
    print "Previous Stable Server: ", mag.getVanillaServer(stable=True, versions_old=1)