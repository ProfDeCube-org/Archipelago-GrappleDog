from typing import Any, ClassVar, Dict, Iterable, List, Mapping, Union

from BaseClasses import CollectionState, Entrance, Item, Location, Region

from test.bases import WorldTestBase
from test.general import gen_steps, setup_multiworld
from test.multiworld.test_multiworlds import MultiworldTestBase

from .. import GrappleDogWorld
from .. import options as ops


class GrappleDogTestBase(WorldTestBase):
    game = "Grapple Dog"
    world: GrappleDogWorld


class TestFixedGadgets(GrappleDogTestBase):
    options: dict[str, Any] = {
        "randomise_gadgets": int(False)
    }

    def test_bosses_have_gadgets(self) -> None:
        self.world_setup()
        for (boss, gadget) in [
            ("Level 1-B: Beat REX", "Cosmic Phone"),
            ("Level 2-B: Beat TANK", "Cosmic Bulb"),
            ("Level 3-B: Beat FACE", "Cosmic Disc"),
            ("Level 4-B: Beat DRGN", "Cosmic Battery"),
        ]:
            item: Item | None = self.multiworld.get_location(boss, self.player).item
            if item is None:
                raise AssertionError(f"Boss {boss!r} has no item")
            self.assertEqual(
                item.name,
                gadget,
                f"Boss {boss!r} should have {gadget!r}, has {item.name!r}"
            )

    def test_hook_not_in_world(self) -> None:
        self.world_setup()
        with self.assertRaises(ValueError):
            self.get_item_by_name("Grapple Hook")


class TestStartWithoutHook(GrappleDogTestBase):
    options: dict[str, Any] = {
        "start_with_hook": int(False)
    }

    def test_hook_in_world(self) -> None:
        self.world_setup()
        self.get_item_by_name("Grapple Hook")


class TestFruitGemChecks(GrappleDogTestBase):
    options: dict[str, Any] = {
        "fruit_gem_one_target": 200,
        "fruit_gem_two_target": 100
    }

    def test_fruit_gem_checks_in_order(self) -> None:
        self.world_setup()
        self.assertEqual(self.world.options.fruit_gem_one_target.value, 100)
        self.assertEqual(self.world.options.fruit_gem_two_target.value, 200)


class TestGoldMedalChecks(GrappleDogTestBase):
    options: dict[str, Any] = {
        "speedrunner_count_one": 3,
        "speedrunner_count_two": 2,
        "speedrunner_count_three": 1
    }

    def test_gold_medal_checks_in_order(self) -> None:
        self.world_setup()
        self.assertEqual(self.world.options.speedrunner_count_one.value, 1)
        self.assertEqual(self.world.options.speedrunner_count_two.value, 2)
        self.assertEqual(self.world.options.speedrunner_count_three.value, 3)


class TestBoomerangBanditChecks(GrappleDogTestBase):
    options: dict[str, Any] = {
        "boomerang_score_one": 30000,
        "boomerang_score_two": 20000,
        "boomerang_score_three": 10000
    }

    def test_boomerang_bandit_checks_in_order(self) -> None:
        self.world_setup()
        self.assertEqual(self.world.options.boomerang_score_one.value, 10000)
        self.assertEqual(self.world.options.boomerang_score_two.value, 20000)
        self.assertEqual(self.world.options.boomerang_score_three.value, 30000)


class TestLevelLockedBosses(GrappleDogTestBase):
    options: dict[str, Any] = {
        "boss_level_unlock": ops.BossLevelUnlock.option_level
    }

    def test_optional_gems_are_filler(self) -> None:
        self.world_setup()
        gems: list[Item] = self.get_items_by_name("Gem")
        self.assertGreaterEqual(len(gems), 1)
        progressions: int = 0
        fillers: int = 0
        for gem in gems:
            progressions += int(gem.advancement)
            fillers += int(gem.filler)
        self.assertEqual(
            progressions,
            0,
            f"No gems should be progression, found {progressions}/{len(gems)}"
        )
        self.assertEqual(
            fillers,
            len(gems),
            f"All gems should be filler, found {fillers}/{len(gems)}"
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
