#!/usr/bin/env python
#
# MinecraftAssetsGetter -> mag0.1
#

DEBUG = False

import urllib2
import re
from datetime import datetime
from xml.dom.minidom import parseString
from operator import itemgetter
import urlparse

import bs4


class MinecraftAssetsGetter:
    # last backslash in fileUrl is important
    def __init__(self, xmlUrl='http://assets.minecraft.net/', fileUrl='http://assets.minecraft.net/'):
        self.fileUrl = fileUrl
        file = urllib2.urlopen(xmlUrl)
        data = file.read()
        file.close()
        self.dom = parseString(data)

    def getVanillaVersionList(self, stable=True):
        """ Returns a list of versions, sorted by date, from earliest to
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
                # Regex: 2 digits, 'w', 2 digits, 1 letter
                if stable and "pre" in version or "rc" in version or re.search("^\d{2}w\d{2}[a-zA-Z]{1}$", version):
                    self.date_list[date] = version
                elif not stable and "pre" in version or "rc" in version or re.search("^\d{2}w\d{2}[a-zA-Z]{1}$", version):
                    self.date_list[date] = version
                if DEBUG:
                    print "add	-> " + version
            else:
                if DEBUG:
                    print "skip 	-> " + version
        #self.sorted_list = self.date_list.sort()
        #if DEBUG:
        #print self.date_list
        sorted_list = list()
        for key in sorted(self.date_list.iterkeys()):
            #print "%s: %s" % (key, self.date_list[key])
            sorted_list.append(self.date_list[key])
        #print "SET: ", set(sorted_list)

        #for item in sorted_list:
            #print item

        # Filter duplicates
        seen = set()
        seen_add = seen.add
        sorted_unique_list = [ x for x in sorted_list if x not in seen and not seen_add(x)]
        #for item in sorted_unique_list:
            #print item
        return sorted_unique_list

    def getBukkitVersionList(self, stable=True):
        """ Returns a list of versions, sorted by date, from earliest to
        latest. versions[-1] would be the latest version.
        stable: Determines whether only stable (recommended) releases are returned or not.

        Each version is a dict with the following keys:
        build_number: Build number with # prepended, used for sorting.
        build_name: Official name of the release
        download_link: Link (minus base URL) for the jar. None if no download link provided,
                       or if build is a broken build.
        """
        # TODO: Make this less fragile!!!
        bukkit_base_url = 'http://dl.bukkit.org/'
        build_list = []
        if stable:
            html = urllib2.urlopen('http://dl.bukkit.org/downloads/craftbukkit/list/rb/').read()
            soup = bs4.BeautifulSoup(html)
            build_rows = soup.find_all('tr', {"class": "chan-rb"})
        else:
            html = urllib2.urlopen('http://dl.bukkit.org/downloads/craftbukkit/list/beta/').read()
            soup = bs4.BeautifulSoup(html)
            build_rows = soup.find_all('tr', {"class": "chan-beta"})

        # Process each row in the table
        for build_row in build_rows:
            build_dict = {}
            # Process the specific row
            for row in build_row:
                for row_elem in row:
                    if isinstance(row_elem, bs4.element.Tag):
                        # Check if it is a link
                        if row_elem.name == 'a':
                            # Check if the link is the download link (has a tool tip)
                            if "class" in row_elem.attrs and row_elem.attrs["class"][0] == 'tooltipd':
                                download_link = urlparse.urljoin(bukkit_base_url, row_elem.attrs["href"])
                                build_dict['download_link'] = download_link
                            else:
                                # Link back to the download page, ignore.
                                if "/downloads/craftbukkit/list/" in row_elem.attrs["href"]:
                                    continue
                                else:
                                    # Grab the text from the link. This is the build number
                                    build_dict['build_number'] = row_elem.string
                    # Plain string, not a link. Find the build_name
                    elif isinstance(row_elem, bs4.element.NavigableString):
                        # Ignore empty strings
                        if row_elem.string == ' ' or row_elem == '\n' or row_elem is None:
                            continue
                        else:
                            # Left over is build_name
                            build_dict['build_name'] = row_elem.string
            # If no download link found, set to None. Cleaner than always check 'in'
            if "download_link" not in build_dict:
                build_dict["download_link"] = None
            build_list.append(build_dict)
        # Sort based on build numbers. Newest builds will be last.
        return sorted(build_list, key=itemgetter('build_number'))

    def getLatestVanillaServer(self, stable=True):
        """ Returns the URL of the latest server version.
        table: Determines whether only stable releases are returned or not.
        """
        version_list = self.getVanillaVersionList(stable)
        return self.getVanillaServerUrl(version_list[-1])

    def getLatestBukkitServer(self, stable=True):
        version_list = self.getBukkitVersionList(stable)
        return version_list[-1]["download_link"]

    def getLatestClient(self, stable=True):
        """ Returns the URL of the latest client version.
        table: Determines whether only stable releases are returned or not.
        """
        version_list = self.getVanillaVersionList(stable)
        #print version_list
        return self.getClientUrl(version_list[-1])

    def getVanillaServer(self, stable=True, versions_old=0):
        """ Returns the URL of the latest server version.
        table: Determines whether only stable releases are returned or not.
        Returns None if too versions old is more than available servers.
        """
        version_list = self.getVanillaVersionList(stable)
        #print len(version_list), ', ', version_list
        if versions_old + 1 > len(version_list):
            return None
        return self.getVanillaServerUrl(version_list[-1 - versions_old])

    def getBukkitServer(self, stable=True, versions_old=0):
        version_list = self.getBukkitVersionList(stable)
        if versions_old + 1 > len(version_list):
            return None
        return version_list[-1 - versions_old]["download_link"]

    def getClient(self, stable=True, versions_old=0):
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
    print "Latest Prerelease Client: ", mag.getLatestClient(stable=False)
    print "Latest Stable Client: ", mag.getLatestClient()
    print "Latest Prerelease Server: ", mag.getLatestVanillaServer(stable=False)
    print "Latest Stable Server: ", mag.getLatestVanillaServer()
    print "Previous Prerelease Server: ", mag.getVanillaServer(stable=False, versions_old=1)
    print "Previous Stable Server: ", mag.getVanillaServer(versions_old=1)
    print "Latest Bukkit Recommended Server: ", mag.getLatestBukkitServer()
    print "Latest Bukkit Beta Server: ", mag.getLatestBukkitServer(stable=False)
    print "Previous Bukkit Recommended Server: ", mag.getBukkitServer(versions_old=1)
    print "Previous Bukkit Beta Server: ", mag.getBukkitServer(stable=False, versions_old=1)
    #print mag.getBukkitVersionList(beta=True)
    #print mag.getBukkitVersionList(beta=False)
