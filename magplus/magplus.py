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
        unsorted_list = []
        for content in contents:
            # Example build_dict
            # {'version': '12w23' or '1_2_5', 'date': '2011-11-24T13:20:06.000Z'}
            build_dict = {}
            key = getText(content.getElementsByTagName("Key")[0].childNodes)
            date = getText(content.getElementsByTagName("LastModified")[0].childNodes)
            try:
                version, file = key.split('/')
                if len(file) == 0:
                    #print key, ", ", key.split('/'), ', ', version
                    continue
            except ValueError:
                continue
            # Ensure this is a JAR
            if file == "minecraft.jar" or file == "minecraft_server.jar":
                # Filter for stable or unstable version
                # Regex: 2 digits, 'w', 2 digits, 1 letter
                if stable and "pre" not in version and "rc" not in version and not re.search("^\d{2}w\d{2}[a-zA-Z]{1}$", version):
                    if DEBUG:
                        print "Adding stable version %s, date %s" % (version, date)
                    build_dict['version'] = version
                    build_dict['date'] = date
                    unsorted_list.append(build_dict)
                elif not stable:
                    if "pre" in version or "rc" in version or re.search("^\d{2}w\d{2}[a-zA-Z]{1}$", version):
                        if DEBUG:
                            print "Adding unstable version %s, date %s" % (version, date)
                        build_dict['version'] = version
                        build_dict['date'] = date
                        unsorted_list.append(build_dict)
                else:
                    #print "Unknown type found. Version %s, date %s" % (version, date)
                    # Caught a stable release with unstable=True or vice versa.
                    continue

        sorted_list = list()
        sorted_list = sorted(unsorted_list, key=itemgetter('date'))
        #for a in sorted_list:
            #print a
        sorted_unique_list = list()
        for b in self.unique_keys(sorted_list):
            #print b
            sorted_unique_list.append(b)

        # Filter duplicates
        #seen = set()
        #seen_add = seen.add
        #sorted_unique_list = [ x for x in sorted_list if x not in seen and not seen_add(x)]
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
        return self.getVanillaServerUrl(version_list[-1]['version'])

    def getLatestBukkitServer(self, stable=True):
        version_list = self.getBukkitVersionList(stable)
        return version_list[-1]["download_link"]

    def getNewerVanillaVersion(self, current_version, stable=True):
        """ Given stable and the current version, attempts to find a newer
        version. Current version must a key in getVanillaVersionList, so
        something like 1_2_5, 12w23, rc2, etc.
        Returns a build_dict {'version', 'date'} or None if current_version
        is up to date.
        Raises SyntaxError if current_version is improperly formatted
        """
        version_list = self.getVanillaVersionList(stable)
        # Find the date of current_version by iterating the list
        current_date = None
        for version in version_list:
            if version['version'] == current_version:
                current_date = version['date']
        # Could not find in list.
        if DEBUG:
            print version_list
        if current_date is None:
            raise SyntaxError("current_version was not found in version list.\
            Either you have an improperly formatted version or a really old version (pre 1.8)")
        latest_version = version_list[-1]
        if latest_version['date'] > current_date:
            return latest_version
        else:
            return None

    def getNewerBukkitVersion(self, current_version, stable=True):
        """ Given stable and the current version, attempts to find a newer
        version. Current version must a key in getVanillaVersionList, so
        something like 1_2_5, 12w23, rc2, etc.
        Returns a build_dict {'version', 'date'} or None if current_version
        is up to date.
        Raises SyntaxError if current_version is improperly formatted
        """
        version_list = self.getBukkitVersionList(stable)
        # Find the date of current_version by iterating the list
        current_build_number = None
        for version in version_list:
            if DEBUG:
                print version['build_name'], current_version
            if version['build_name'] == current_version:
                current_build_number = version['build_number']
        # Could not find in list.
        if current_build_number is None:
            raise SyntaxError("current_version was not found in version list.\
            Either you have an improperly formatted version or a really old version (pre 1.8)")
        latest_version = version_list[-1]
        if latest_version['build_number'] > current_build_number:
            return latest_version
        else:
            return None

    def getLatestClient(self, stable=True):
        """ Returns the URL of the latest client version.
        table: Determines whether only stable releases are returned or not.
        """
        version_list = self.getVanillaVersionList(stable)
        #print version_list
        return self.getClientUrl(version_list[-1]['version'])

    def getVanillaServer(self, stable=True, versions_old=0):
        """ Returns the URL of the latest server version.
        table: Determines whether only stable releases are returned or not.
        Returns None if too versions old is more than available servers.
        """
        version_list = self.getVanillaVersionList(stable)
        #print len(version_list), ', ', version_list
        if versions_old + 1 > len(version_list):
            return None
        return self.getVanillaServerUrl(version_list[-1 - versions_old]['version'])

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
        return self.getClientUrl(version_list[-1 - versions_old]['version'])

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

    def unique_keys(self, items):
        seen = set()
        for item in items:
            key = item['version']
            if key not in seen:
                seen.add(key)
                yield item
            else:
                # its a duplicate key, drop.
                pass


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
    print "Vanilla Version List: ", mag.getVanillaVersionList(stable=False)
    print "Bukkit Stable Version List: ", mag.getBukkitVersionList(stable=True)
    print "Bukkit Unstable Version List: ", mag.getBukkitVersionList(stable=False)
    print "Newer Unstable Vanilla Version? Yes: ", mag.getNewerVanillaVersion('12w22a', False)
    print "Newer Stable Vanilla Version? Yes: ", mag.getNewerVanillaVersion('1_2', True)
    print "Newer Stable Vanilla Version? No. ", mag.getNewerVanillaVersion('1_2_5', True)
    print "Newer Unstable Bukkit Version? Yes: ", mag.getNewerBukkitVersion('1.2.3-R0.1', False)
    print "Newer Stable Bukkit Version? Yes: ", mag.getNewerBukkitVersion('1.1-R1', True)
    print "Newer Stable Bukkit Version? No. ", mag.getNewerBukkitVersion('1.2.5-R4.0', True)
