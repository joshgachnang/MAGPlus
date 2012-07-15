=========================
MinecraftAssetsGetterPlus
=========================

MinecraftAssetsGetterPlus is a script that parses the XML of http://assets.minecraft.org to find the most recent
version of vanilla Minecraft, either the latest stable or prerelease version. It is a fork of
https://bitbucket.org/Knoppo/mag.

Usage often looks like this::

    from magplus.magplus import MinecraftAssetsGetter

    mag = MinecraftAssetsGetter()
    print "Latest Prerelease Server: ", mag.getLatestServer()
    print "Latest Prerelease Client: ", mag.getLatestClient()
    print "Latest Stable Server: ", mag.getLatestServer(stable=True)
    print "Latest Stable Client: ", mag.getLatestClient(stable=True)
    print "Previous Prerelease Server: ", mag.getServer(versions_old=1)
    print "Previous Stable Server: ", mag.getServer(stable=True, versions_old=1)

Todo
====

* Add support for Bukkit servers

License
=======

This project is released under the GPLv2.

Thanks
======

Thanks to `Knoppo <https://bitbucket.org/Knoppo>`_ for writing the original version.