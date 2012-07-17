import unittest
import urllib2
from magplus import MinecraftAssetsGetter


latest_stable_bukkit = '1.2.5-R4.0'
latest_unstable_bukkit = '1.2.5-R1.3'
latest_stable_vanilla = '1_2_5'
latest_unstable_vanilla = '12w27a'

class TestMAG(unittest.TestCase):
    def setUp(self):
        self.mag = MinecraftAssetsGetter()

    def exists(self, url):
        try:
            f = urllib2.urlopen(urllib2.Request(url))
            return True
        except:
            print "Could not find URL: ", url
            return False
    def test_latest_prerelease_client(self):
        self.assertTrue(self.exists(self.mag.getLatestClient(stable=False)))

    def test_latest_stable_client(self):
        self.assertTrue(self.exists(self.mag.getLatestClient()))

    def test_latest_vanilla_stable_server(self):
        self.assertTrue(self.exists(self.mag.getLatestVanillaServer()))

    def test_latest_vanilla_prerelease_server(self):
        self.assertTrue(self.exists(self.mag.getLatestVanillaServer(stable=False)))

    def test_previous_vanilla_stable_server(self):
        self.assertTrue(self.exists(self.mag.getVanillaServer(versions_old=1)))

    def test_previous_vanilla_prerelease_server(self):
        self.assertTrue(self.exists(self.mag.getVanillaServer(stable=False, versions_old=1)))

    def test_latest_bukkit_stable_server(self):
        self.assertTrue(self.exists(self.mag.getLatestBukkitServer()))

    def test_latest_bukkit_prerelease_server(self):
        self.assertTrue(self.exists(self.mag.getLatestBukkitServer(stable=False)))

    def test_previous_bukkit_stable_server(self):
        self.assertTrue(self.exists(self.mag.getBukkitServer(versions_old=1)))

    def test_previous_bukkit_prerelease_server(self):
        self.assertTrue(self.exists(self.mag.getBukkitServer(stable=False, versions_old=1)))

    def test_latest_stable_vanilla(self):
        self.assertTrue(self.mag.getNewerVanillaVersion('1_2', True)['version'] == latest_stable_vanilla)
        self.assertTrue(self.mag.getNewerVanillaVersion(latest_stable_vanilla, True) == None)

    def test_latest_unstable_vanilla(self):
        self.assertTrue(self.mag.getNewerVanillaVersion('12w22a', False)['version'] == latest_unstable_vanilla)
        self.assertTrue(self.mag.getNewerVanillaVersion(latest_unstable_vanilla, False) == None)

    def test_latest_stable_bukkit(self):
        self.assertTrue(self.mag.getNewerBukkitVersion('1.2.5-R3.0', True)['build_name'] == latest_stable_bukkit)
        self.assertTrue(self.mag.getNewerBukkitVersion(latest_stable_bukkit, True) == None)

    def test_latest_unstable_bukkit(self):
        self.assertTrue(self.mag.getNewerBukkitVersion('1.2.5-R1.2', False)['build_name'] == latest_unstable_bukkit)
        self.assertTrue(self.mag.getNewerBukkitVersion(latest_unstable_bukkit, False) == None)


if __name__ == '__main__':
    print "If you are getting a lot of failures, try updating the settings at the top of this file."
    unittest.main()
