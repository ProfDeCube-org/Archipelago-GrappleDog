from typing import Any, List, Optional, Set
from Options import Option
import Utils
import os
import json

from BaseClasses import ItemClassification, Region, Tutorial, Item, Location, MultiWorld
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, icon_paths, launch as launch_component, Type
from .items import GrappleDogItem, item_data_table, item_table
from .locations import GrappleDogLocation, location_data_table, location_table, all_levels, location_groups
from .options import GrappleDogOptions, option_groups
from .regions import region_data_table
from .rules import create_rules, evaluate_requirement, check_fruit_for_level
from .movement_rules import movement_rules
from .npc_sanity_rules import npc_sanity_rules

def launch_client(*args: str):
    from .Client import launch
    launch_component(launch, name="PTClient", args=args)


components.append(Component("Grapple Dog Client", func=launch_client, component_type=Type.CLIENT, icon="grappledog"))

icon_paths["grappledog"] = f"ap:{__name__}/grappledog.png"

class GrappleDogWebWorld(WebWorld):
    theme = "partyTime"
    ut_can_gen_without_yaml = True

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing GrappleDog.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["ProfDeCube"]
    )
    tutorials = [setup_en]
    option_groups = option_groups
    

class GrappleDogWorld(World):
    """A dog with a grappling hook, what more do you want"""

    game = "Grapple Dog"
    web = GrappleDogWebWorld()
    options: GrappleDogOptions
    options_dataclass = GrappleDogOptions
    location_name_to_id = location_table
    item_name_to_id = item_table
    starting_items = []
    item_name_groups = {'Abilities': {'Grapple Hook', 'Climb', 'Wall Jump', 'Slam', 'Swim', 'Double Jump'}, 'Objects': {'Cannons', 'Balloons', 'Bounce Pads', 'Carrots'}, 'Gadgets': {'Cosmic Bulb', 'Cosmic Phone', 'Cosmic Battery', 'Cosmic Disc'}, 'Worlds': {'World 4', 'World 3', 'World 6', 'World 5', 'World 2', 'World 1'}, 'Stages': {'Bonus 2-2', 'Level 1-5', 'Level 3-2', 'Level 5-B', 'Level 2-2', 'Bonus 2-1', 'Level 4-5', 'Bonus 3-2', 'Level 4-1', 'Bonus 3-3', 'Level 4-B', 'Level 4-2', 'Level 3-4', 'Level 1-4', 'Level 2-4', 'Bonus 1-4', 'Level 4-3', 'Level 2-5', 'Level 4-4', 'Bonus 6-3', 'Level 1-3', 'Bonus 1-2', 'Level 2-1', 'Bonus 5-4', 'Bonus 4-3', 'Bonus 3-1', 'Level 1-1', 'Bonus 3-4', 'Bonus 5-1', 'Level 5-5', 'Level 1-B', 'Level 2-3', 'Bonus 2-4', 'Level 2-B', 'Level 3-5', 'Level 1-2', 'Bonus 4-2', 'Bonus 1-3', 'Level 6-1', 'Level 5-2', 'Level 3-1', 'Level 5-4', 'Bonus 1-1', 'Level 5-1', 'Bonus 5-2', 'Bonus 5-3', 'Level 6-3', 'Level 3-B', 'Bonus 6-1', 'Level 3-3', 'Bonus 4-4', 'Level 5-3', 'Bonus 2-3', 'Bonus 6-2', 'Bonus 4-1', 'Level 6-2'}, 'Bonuses': {'Bonus 2-2', 'Bonus 2-1', 'Bonus 3-2', 'Bonus 3-3', 'Bonus 1-4', 'Bonus 6-3', 'Bonus 1-2', 'Bonus 5-4', 'Bonus 4-3', 'Bonus 3-1', 'Bonus 5-1', 'Bonus 3-4', 'Bonus 2-4', 'Bonus 4-2', 'Bonus 1-3', 'Bonus 1-1', 'Bonus 5-2', 'Bonus 5-3', 'Bonus 6-1', 'Bonus 4-4', 'Bonus 6-2', 'Bonus 2-3', 'Bonus 4-1'}, 'Levels': {'Level 1-5', 'Level 3-2', 'Level 5-B', 'Level 2-2', 'Level 4-5', 'Level 4-1', 'Level 4-B', 'Level 4-2', 'Level 3-4', 'Level 1-4', 'Level 2-4', 'Level 4-3', 'Level 2-5', 'Level 4-4', 'Level 1-3', 'Level 2-1', 'Level 1-1', 'Level 5-5', 'Level 1-B', 'Level 2-3', 'Level 3-5', 'Level 2-B', 'Level 1-2', 'Level 6-1', 'Level 5-2', 'Level 3-1', 'Level 5-4', 'Level 5-1', 'Level 6-3', 'Level 3-B', 'Level 3-3', 'Level 5-3', 'Level 6-2'}, 'Features': {'Cannons', 'Balloons', 'Grapple Hook', 'Climb', 'Double Jump', 'Bounce Pads', 'Slam', 'Swim', 'Wall Jump', 'Carrots'}}
    location_name_groups = location_groups
    

    def generate_early(self):
        max_boss_gems_needed = max(self.options.gems_for_boss_one.value, self.options.gems_for_boss_two.value, self.options.gems_for_boss_three.value, self.options.gems_for_boss_four.value, self.options.gems_for_boss_five.value)
        self.options.minimum_gems_in_pool.value = max(self.options.minimum_gems_in_pool.value, max_boss_gems_needed)
        self.extra_gems = self.options.minimum_gems_in_pool.value - max_boss_gems_needed

        # Re-order numbered options if out of order
        sort_values: list[int] = sorted([
            self.options.fruit_gem_one_target.value,
            self.options.fruit_gem_two_target.value
        ])
        self.options.fruit_gem_one_target.value = sort_values[0]
        self.options.fruit_gem_two_target.value = sort_values[1]
        sort_values = sorted([
            self.options.speedrunner_count_one.value,
            self.options.speedrunner_count_two.value,
            self.options.speedrunner_count_three.value
        ])
        self.options.speedrunner_count_one.value = sort_values[0]
        self.options.speedrunner_count_two.value = sort_values[1]
        self.options.speedrunner_count_three.value = sort_values[2]
        sort_values = sorted([
            self.options.boomerang_score_one.value,
            self.options.boomerang_score_two.value,
            self.options.boomerang_score_three.value
        ])
        self.options.boomerang_score_one.value = sort_values[0]
        self.options.boomerang_score_two.value = sort_values[1]
        self.options.boomerang_score_three.value = sort_values[2]

        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Get the passed through slot data from the real generation
            genned_slot_data: dict[str, Any] = re_gen_passthrough[self.game]

            slot_options: dict[str, Any] = genned_slot_data.get("tracker_options", {})
            # Set all your options here instead of getting them from the yaml
            for key, value in slot_options.items():
                opt: Optional[Option] = getattr(self.options, key, None)
                if opt is not None:
                    # You can also set .value directly but that won't work if you have OptionSets
                    setattr(self.options, key, opt.from_any(value))


    def fill_slot_data(self):
            """
            make slot data, which consists of options, and some other variables.
            """
            grapple_dog_options = self.options.as_dict(
                "starting_health",
                "check_banking",
                "boss_level_unlock",
                "require_gadgets_for_final_boss",
                "level_progression",
                "movement_rando",
                "npc_sanity"
            )
            
            grapple_dog_tracker_options = self.options.as_dict(
                "check_banking",
                "boss_level_unlock",
                "require_gadgets_for_final_boss",
                "level_progression",
                "movement_rando",
                "npc_sanity",
                "fruit_gem_one_target",
                "fruit_gem_two_target",
                "speedrunner_count_one",
                "speedrunner_count_two",
                "speedrunner_count_three",
                "gems_for_boss_one",
                "gems_for_boss_two",
                "gems_for_boss_three",
                "gems_for_boss_four",
                "gems_for_boss_five"
            )
            
            return {
                **grapple_dog_options,
                "tracker_options": {
                    **grapple_dog_tracker_options,
                },
                "speedrun_medals": [
                    self.options.speedrunner_count_one.value,
                    self.options.speedrunner_count_two.value,
                    self.options.speedrunner_count_three.value,
                ],
                "fruit_goals": [
                    self.options.fruit_gem_one_target.value,
                    self.options.fruit_gem_two_target.value
                ],
                "boomerang_scores": [
                    self.options.boomerang_score_one.value,
                    self.options.boomerang_score_two.value,
                    self.options.boomerang_score_three.value
                ],
                "boss_gems": [
                    self.options.gems_for_boss_one.value,
                    self.options.gems_for_boss_two.value,
                    self.options.gems_for_boss_three.value,
                    self.options.gems_for_boss_four.value,
                    self.options.gems_for_boss_five.value
                ],
                "world_version": "0.1.0",
            }

    def create_item(
        self, name: str, type_override: ItemClassification | None = None
    ) -> GrappleDogItem:
        classification: ItemClassification = item_data_table[name].type
        if type_override is not None:
            classification = type_override

        return GrappleDogItem(
            name, classification, item_data_table[name].code, self.player
        )

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # Trigger a regen in UT
        return slot_data

    def create_items(self) -> None:
        made_gem_count = 0
        self.starting_items = []
        item_pool: List[GrappleDogItem] = []
        levels_to_pick_from = all_levels.copy()
        
        if(self.options.start_with_hook):
            self.multiworld.push_precollected(self.create_item('Grapple Hook'))
        for i in range(self.options.starting_health.value):
            self.multiworld.push_precollected(self.create_item('Max Health Up'))
        if(self.options.boss_level_unlock == 0):
            self.options.starting_levels.value = min(self.options.starting_levels.value, 51)
            self.multiworld.push_precollected(self.create_item('Level 1-B'))
            levels_to_pick_from.remove('Level 1-B')
            self.multiworld.push_precollected(self.create_item('Level 2-B'))
            levels_to_pick_from.remove('Level 2-B')
            self.multiworld.push_precollected(self.create_item('Level 3-B'))
            levels_to_pick_from.remove('Level 3-B')
            self.multiworld.push_precollected(self.create_item('Level 4-B'))
            levels_to_pick_from.remove('Level 4-B')
            self.multiworld.push_precollected(self.create_item('Level 5-B'))
            levels_to_pick_from.remove('Level 5-B')
        for i in range(self.options.starting_levels):
            chosen_level = self.multiworld.random.choice(levels_to_pick_from)
            levels_to_pick_from.remove(chosen_level)
            self.multiworld.push_precollected(self.create_item(chosen_level))

        exclude = [item.name for item in self.multiworld.precollected_items[self.player]]

        for key, item in item_data_table.items():
            if item.code and item.can_create(self):
                for _ in range(item.count(self)):
                    if key in exclude:
                        exclude.remove(key)
                    elif key == "Gem":
                        type_override: ItemClassification = ItemClassification.filler
                        if (
                            self.options.boss_level_unlock.value != 2 and
                            made_gem_count < self.options.minimum_gems_in_pool.value
                        ):
                            if self.multiworld.worlds[self.player].options.accessibility == "minimal":
                                type_override = (
                                    ItemClassification.progression_deprioritized_skip_balancing
                                )
                            else:
                                type_override = (
                                    ItemClassification.progression_skip_balancing
                                )
                        item_pool.append(self.create_item(key, type_override))
                        made_gem_count += 1
                    else:
                        item_pool.append(self.create_item(key))

        if(not self.options.start_with_hook.value):
            self.multiworld.early_items[self.player]["Grapple Hook"] = 1
                        
        
        if(self.options.movement_rando.value):
            potential_early_unwalls = ["Bonus 1-2", "Level 2-5", "Bonus 2-1", "Bonus 6-3", "Bounce Pads", "Swim", "Wall Jump"]
            
            chosen_unwall_one = self.multiworld.random.choice(potential_early_unwalls)
            potential_early_unwalls.remove(chosen_unwall_one)
            
            chosen_unwall_two = self.multiworld.random.choice(potential_early_unwalls)
            potential_early_unwalls.remove(chosen_unwall_two)
            chosen_unwall_three = self.multiworld.random.choice(potential_early_unwalls)
            potential_early_unwalls.remove(chosen_unwall_three)
            self.multiworld.early_items[self.player][chosen_unwall_one] = 1
            self.multiworld.early_items[self.player][chosen_unwall_two] = 1
            self.multiworld.early_items[self.player][chosen_unwall_three] = 1

                        
        un_filled_loc_size = len(self.multiworld.get_unfilled_locations(self.player))
        while len(item_pool) < un_filled_loc_size:
            item_pool.append(self.create_filler())
            
        self.multiworld.itempool += item_pool

    def fill_hook(self, progitempool, a, b, c,):
        progitempool.sort(key = lambda item: item.player == self.player and item.name == "Gem")

    def create_regions(self) -> None:

        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.get_region(region_name)
            for location_name, location_data in location_data_table.items():
                if location_data.region == region_name and location_data.can_create(self):
                    region.add_locations({location_name: location_data.address}, GrappleDogLocation)
                    if "Fruit Gem" in location_name:
                        if not bool(self.options.movement_rando.value):
                            continue
                        fruit_gem: str = location_name.split(" ")[-1]
                        target: int
                        if fruit_gem == "1":
                            target = self.options.fruit_gem_one_target.value
                        else:
                            target = self.options.fruit_gem_two_target.value
                        level: str = location_name.split(": ")[0]
                        self.multiworld.get_location(location_name, self.player).access_rule = lambda state, level=level, player=self.player, target=target: check_fruit_for_level(state, level, player) >= target
                        # self.multiworld.get_location(location_name, self.player).access_rule = lambda state, player=self.player: evaluate_requirement("Grapple Hook + Bounce Pads + Balloons + Cannons + Carrots + Wall Jump + Climb + Swim + Slam", state, player)
        
        if(not self.options.randomise_gadgets and self.options.require_gadgets_for_final_boss):
                self.multiworld.get_location("Level 1-B: Beat REX", self.player).place_locked_item(self.create_item("Cosmic Phone"))
                self.multiworld.get_location("Level 2-B: Beat TANK", self.player).place_locked_item(self.create_item("Cosmic Bulb"))
                self.multiworld.get_location("Level 3-B: Beat FACE", self.player).place_locked_item(self.create_item("Cosmic Disc"))
                self.multiworld.get_location("Level 4-B: Beat DRGN", self.player).place_locked_item(self.create_item("Cosmic Battery"))
                
        if(self.options.movement_rando.value):
            for location, rule in movement_rules["INSTANT"].items():
                self.multiworld.get_location(location, self.player).access_rule = lambda state, rule=rule, player=self.player: evaluate_requirement(rule, state, player)
        
            if(self.options.npc_sanity.value):
                for location, rule in npc_sanity_rules.items():
                    self.multiworld.get_location(location, self.player).access_rule = lambda state, rule=rule, player=self.player: evaluate_requirement(rule, state, player)
        
        
        self.multiworld.get_location("Level 5-B: Beat NUL", self.player).place_locked_item(self.create_item("Kiss From Rabbit"))

    def set_rules(self):
        create_rules(self)

    def get_filler_item_name(self) -> str:
        return "Dog Biscuit"
