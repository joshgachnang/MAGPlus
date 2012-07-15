=========================
MinecraftAssetsGetterPlus
=========================

MinecraftAssetsGetterPlus is a script that parses the XML of http://assets.minecraft.org to find the most recent
version of vanilla Minecraft, either the latest stable or prerelease version. It is a fork of
https://bitbucket.org/Knoppo/mag.

Usage often looks like this::

    from magplus.magplus import MinecraftAssetsGetter

    mag = MinecraftAssetsGetter()
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

Todo
====

* Make getBukkitVersionList() less fragile. It works now, but who knows for how long.

Changes
=======

0.1.2, 07/15/2012 -- Fixed ordering issues that were returning the wrong versions.

0.1.1, 07/15/2012 -- Testing addition of Bukkit version listing. Added new functions for Bukkit. Requires BeautifulSoup4 now.

0.1.0, 07/14/2012 -- Fixed minor bugs with packaging. Some files were not being included.

0.0.9, 07/14/2012 -- Initial release.

License
=======

This project is released under the GPLv2.

Thanks
======

Thanks to `Knoppo <https://bitbucket.org/Knoppo>`_ for writing the original version.