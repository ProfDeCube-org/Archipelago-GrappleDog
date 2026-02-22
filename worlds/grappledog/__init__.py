from typing import List, Set
import Utils
import os
import json

from BaseClasses import LocationProgressType, Region, Tutorial, ItemClassification, Item
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, icon_paths, launch as launch_component, Type
from worlds.generic.Rules import set_rule
from .items import GrappleDogItem, item_data_table, item_table
from .locations import GrappleDogLocation, location_data_table, location_table, all_levels, hook_possible_locations
from .options import GrappleDogOptions, option_groups
from .regions import region_data_table
from .rules import create_rules, evaluate_requirement, check_fruit_for_level

def launch_client(*args: str):
    from .Client import launch
    launch_component(launch, name="PTClient", args=args)
    
    
with open(os.path.join(os.path.dirname(__file__), 'movement_rules.json'), 'r') as file:
    movement_rules = json.load(file)


components.append(Component("Grapple Dog Client", "GDClient", func=launch_client, component_type=Type.CLIENT, icon="grappledog"))

icon_paths["grappledog"] = f"ap:{__name__}/grappledog.png"

class GrappleDogWebWorld(WebWorld):
    theme = "partyTime"

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
    

    def generate_early(self):
        self.options.minimum_gems_in_pool.value = max(self.options.minimum_gems_in_pool.value, self.options.gems_for_boss_one.value)
        self.options.minimum_gems_in_pool.value = max(self.options.minimum_gems_in_pool.value, self.options.gems_for_boss_two.value)
        self.options.minimum_gems_in_pool.value = max(self.options.minimum_gems_in_pool.value, self.options.gems_for_boss_three.value)
        self.options.minimum_gems_in_pool.value = max(self.options.minimum_gems_in_pool.value, self.options.gems_for_boss_four.value)
        self.options.minimum_gems_in_pool.value = max(self.options.minimum_gems_in_pool.value, self.options.gems_for_boss_five.value)


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
                "movement_rando"
            )
            
            return {
                **grapple_dog_options,
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
                
    def create_item(self, name: str) -> GrappleDogItem:
        return GrappleDogItem(name, item_data_table[name].type, item_data_table[name].code, player=self.player)

    def create_items(self) -> None:
        self.starting_items = []
        item_pool: List[GrappleDogItem] = []
        level_items = []
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
            if(key.startswith("Level")):
                level_items.append(key)
            if item.code and item.can_create(self):
                for i in range(item.count(self)):
                    if(key in exclude):
                        exclude.remove(key)
                    else:
                        item_pool.append(self.create_item(key))
                        
                        
        if(not self.options.start_with_hook):
            self.multiworld.early_items[self.player]["Grapple Hook"] = 1
                        
        self.item_name_groups = {
            "Gadgets": {"Gadget 1", "Gadget 2", "Gadget 3", "Gadget 4"},
            "Worlds": {"World 1", "World 2", "World 3", "World 4", "World 5", "World 6"},
            "Levels": tuple(level_items)
        }
                        
        un_filled_loc_size = len(self.multiworld.get_unfilled_locations(self.player))
        while len(item_pool) < un_filled_loc_size:
            item_pool.append(self.create_filler())
            
        self.multiworld.itempool += item_pool
        

    def create_regions(self) -> None:
        
        level_complete_set = set()
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
                    if("Level Complete" in location_name):
                        level_complete_set.add(location_name)
                    if(self.options.movement_rando.value and "Fruit Gem" in location_name):
                        level = ""
                        target = 0
                        if("Fruit Gem 1" in location_name):
                            level = location_name.replace("Fruit Gem 1 (", "").replace(")", "")
                            target = self.options.fruit_gem_one_target.value
                        else:
                            level = location_name.replace("Fruit Gem 2 (", "").replace(")", "")
                            target = self.options.fruit_gem_two_target.value
                        self.multiworld.get_location(location_name, self.player).access_rule = lambda state, level=level, player=self.player, target=target: check_fruit_for_level(state, level, player) >= target
                        # self.multiworld.get_location(location_name, self.player).access_rule = lambda state, player=self.player: evaluate_requirement("Grapple Hook + Bounce Pads + Balloons + Cannons + Carrots + Wall Jump + Climb + Swim + Slam", state, player)

        
        self.location_name_groups = {"Completes": level_complete_set}
        if(not self.options.randomise_gadgets and self.options.require_gadgets_for_final_boss):
                self.multiworld.get_location("Beat REX", self.player).place_locked_item(self.create_item("Gadget 1"))
                self.multiworld.get_location("Beat TANK", self.player).place_locked_item(self.create_item("Gadget 2"))
                self.multiworld.get_location("Beat FACE", self.player).place_locked_item(self.create_item("Gadget 3"))
                self.multiworld.get_location("Beat DRGN", self.player).place_locked_item(self.create_item("Gadget 4"))
                # self.multiworld.get_location("Level Complete (Level 1-1)", self.player).place_locked_item(self.create_item("Gadget 4"))
                
        if(self.options.movement_rando.value):
            for location, rule in movement_rules["INSTANT"].items():
                self.multiworld.get_location(location, self.player).access_rule = lambda state, rule=rule, player=self.player: evaluate_requirement(rule, state, player)
        
        
        self.multiworld.get_location("Defeat NUL", self.player).place_locked_item(self.create_item("Kiss From Rabbit"))

    def set_rules(self):
        create_rules(self)

    def get_filler_item_name(self) -> str:
        return "Dog Biscuit"
