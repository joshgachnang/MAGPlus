import unittest
import urllib2
from magplus import MinecraftAssetsGetter


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

if __name__ == '__main__':
    unittest.main()
