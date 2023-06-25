import unittest
from unittest.mock import MagicMock

from src.data_utils.pool import Pool, TurtlePool, PuppyPool, StarPool, GoldenPool, get_pack


class TestPool(unittest.TestCase):
    def setUp(self) -> None:
        self.pool = Pool()
        print("\n")

        self.pack_samples = {
            "Turtle": {
                1: ["Ant", "Sloth", "Horse"],
                2: ["Crab", "Swan", "Flamingo"],
                3: ["Badger", "Snail", "Dolphin"],
                4: ["Bison", "Worm", "Penguin"],
                5: ["Cow", "Turkey", "Scorpion"],
                6: ["Boar", "Tiger", "Leopard"]
            },
            "Puppy": {  # First, Last, and random alphabetically
                1: ["Ant", "Sloth", "Beetle"],
                2: ["Bat", "Tabby Cat", "Flamingo"],
                3: ["Blowfish", "Tropical Fish", "Owl"],
                4: ["Bison", "Worm", "Llama"],
                5: ["Cow", "Seal", "Microbe"],
                6: ["Boar", "Tyrannosaurus", "Mammoth"],
            },
            "Star": {  # First, Last, and random alphabetically
                1: ["Cockroach", "Seahorse", "Iguana"],
                2: ["Atlantic Puffin", "Yak", "Jellyfish"],
                3: ["Blobfish", "Woodpecker", "Starfish"],
                4: ["Anteater", "Praying Mantis", "Orangutan"],
                5: ["Fox", "Zebra", "Shoebill"],
                6: ["Hammershark", "Velociraptor", "Orca"],
            },
            "Golden": {  # First, Last, and random alphabetically
                1: ["Bulldog", "Silkmoth", "Magpie"],
                2: ["African Penguin", "Stoat", "Gazelle"],
                3: ["Baboon", "Weasel", "Guineafowl"],
                4: ["Cuttlefish", "Vaquita", "Slug"],
                5: ["Beluga Whale", "Wolf", "Emu"],
                6: ["Bird Of Paradise", "Wildebeest", "Cobra"],
            }
        }

    def test_init(self):
        pass

    def test_get_pets_by_pack(self):
        """
        Audits the first and last pets for each tier (alphabetically) and a random middle one.
        Does not check Tiger Pack as it is the special Weekly pack that changes.
        :return:
        """
        packs_to_check = ["Turtle", "Puppy", "Golden", "Star"]
        for pack in packs_to_check:
            self.pool.get_pets_by_pack(pack)
            checks = self.pack_samples[pack]
            for tier, pets in self.pool.pool_dict.items():
                pets = sorted(pets)
                self.assertEqual(pets[0], checks[tier][0])
                self.assertEqual(pets[-1], checks[tier][1])
                self.assertIn(checks[tier][2], pets)

    def test_generate_pet(self):
        self.pool.pool_dict = self.pack_samples["Turtle"]
        for i in range(1, 7):
            # Check specific tier selected
            self.assertIn(self.pool.generate_pet(i, i).name, self.pack_samples["Turtle"][i])
            # Check tier range selected
            self.assertLessEqual(self.pool.generate_pet(1, i).tier, i)
            self.assertGreaterEqual(self.pool.generate_pet(i, 6).tier, i)

    def test_generate_team(self):

        self.pool.pool_dict = self.pack_samples["Turtle"]
        action_handler = MagicMock()
        team_size = 1
        tier_min = 1
        tier_max = 1
        for size in range(1, 6):
            team = self.pool.generate_team(action_handler=action_handler, team_size=team_size, tier_min=tier_min,
                                           tier_max=tier_max)

            self.assertEqual(team.length, team_size)
        self.assertEqual(team.action_handler, action_handler)

    def test_get_pack(self):
        pools = [TurtlePool, PuppyPool, StarPool, GoldenPool]
        pack_names = ["turtle", "puppy", "star", "GOLDEN"]
        for i in range(len(pack_names)):
            self.assertIsInstance(get_pack(pack_names[i]), pools[i])

