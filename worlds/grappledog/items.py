from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import GrappleDogWorld


class GrappleDogItem(Item):
    game = "GrappleDog"


class GrappleDogItemData(NamedTuple):
    count: Callable[["GrappleDogWorld"], int] = lambda world: 1
    code: Optional[int] = None
    name: Optional[str] = None
    type: ItemClassification = ItemClassification.filler
    can_create: Callable[["GrappleDogWorld"], bool] = lambda world: True


item_data_table: Dict[str, GrappleDogItemData] = {
    "Gem": GrappleDogItemData(code=1,type=ItemClassification.skip_balancing, count=lambda world: world.options.minimum_gems_in_pool.value),
    "Dog Biscuit": GrappleDogItemData(code=2,type=ItemClassification.filler, can_create=lambda world: False),
    "Kiss From Rabbit": GrappleDogItemData(code=3,type=ItemClassification.progression, can_create=lambda world: False),
    
    "Grapple Hook": GrappleDogItemData(code=10,type=ItemClassification.progression | ItemClassification.useful, can_create=lambda world: world.options.movement_rando.value),
    "Double Jump": GrappleDogItemData(code=11,type=ItemClassification.useful),
    "Max Health Up": GrappleDogItemData(code=12,type=ItemClassification.useful, count=lambda world: world.options.max_health),
    
    "World 1": GrappleDogItemData(code=21,type=ItemClassification.progression, can_create=lambda world: False ),#world.options.level_progression.value != 0),
    "World 2": GrappleDogItemData(code=22,type=ItemClassification.progression, can_create=lambda world: False ),#world.options.level_progression.value != 0),
    "World 3": GrappleDogItemData(code=23,type=ItemClassification.progression, can_create=lambda world: False ),#world.options.level_progression.value != 0),
    "World 4": GrappleDogItemData(code=24,type=ItemClassification.progression, can_create=lambda world: False ),#world.options.level_progression.value != 0),
    "World 5": GrappleDogItemData(code=25,type=ItemClassification.progression, can_create=lambda world: False ),#world.options.level_progression.value != 0),
    "World 6": GrappleDogItemData(code=26,type=ItemClassification.progression, can_create=lambda world: False ),#world.options.level_progression.value != 0),

    "Bounce Pads": GrappleDogItemData(code=31,type=ItemClassification.progression | ItemClassification.useful, can_create=lambda world: world.options.movement_rando.value),
    "Balloons": GrappleDogItemData(code=32,type=ItemClassification.progression | ItemClassification.useful, can_create=lambda world: world.options.movement_rando.value),
    "Cannons": GrappleDogItemData(code=33,type=ItemClassification.progression | ItemClassification.useful, can_create=lambda world: world.options.movement_rando.value),
    "Carrots": GrappleDogItemData(code=34,type=ItemClassification.progression | ItemClassification.useful, can_create=lambda world: world.options.movement_rando.value),
    "Wall Jump": GrappleDogItemData(code=35,type=ItemClassification.progression | ItemClassification.useful, can_create=lambda world: world.options.movement_rando.value),
    "Climb": GrappleDogItemData(code=36,type=ItemClassification.progression | ItemClassification.useful, can_create=lambda world: world.options.movement_rando.value),
    # "Sprint": GrappleDogItemData(code=37,type=ItemClassification.progression, can_create=lambda world: world.options.movement_rando.value),
    "Swim": GrappleDogItemData(code=38,type=ItemClassification.progression | ItemClassification.useful, can_create=lambda world: world.options.movement_rando.value),
    "Slam": GrappleDogItemData(code=39,type=ItemClassification.progression | ItemClassification.useful, can_create=lambda world: world.options.movement_rando.value),
    
    "Gadget 1": GrappleDogItemData(code=51,type=ItemClassification.progression_skip_balancing, can_create=lambda world: world.options.require_gadgets_for_final_boss and world.options.randomise_gadgets.value),
    "Gadget 2": GrappleDogItemData(code=52,type=ItemClassification.progression_skip_balancing, can_create=lambda world: world.options.require_gadgets_for_final_boss and world.options.randomise_gadgets.value),
    "Gadget 3": GrappleDogItemData(code=53,type=ItemClassification.progression_skip_balancing, can_create=lambda world: world.options.require_gadgets_for_final_boss and world.options.randomise_gadgets.value),
    "Gadget 4": GrappleDogItemData(code=54,type=ItemClassification.progression_skip_balancing, can_create=lambda world: world.options.require_gadgets_for_final_boss and world.options.randomise_gadgets.value),
    
    "Level 1-1": GrappleDogItemData(code=101,type=ItemClassification.progression),
    "Level 1-2": GrappleDogItemData(code=102,type=ItemClassification.progression),
    "Level 1-3": GrappleDogItemData(code=103,type=ItemClassification.progression),
    "Level 1-4": GrappleDogItemData(code=104,type=ItemClassification.progression),
    "Level 1-5": GrappleDogItemData(code=105,type=ItemClassification.progression),
    "Level 1-B": GrappleDogItemData(code=106,type=ItemClassification.progression_skip_balancing, can_create=lambda world: world.options.boss_level_unlock > 0),
    "Bonus 1-1": GrappleDogItemData(code=111,type=ItemClassification.progression),
    "Bonus 1-2": GrappleDogItemData(code=112,type=ItemClassification.progression),
    "Bonus 1-3": GrappleDogItemData(code=113,type=ItemClassification.progression),
    "Bonus 1-4": GrappleDogItemData(code=114,type=ItemClassification.progression),
    
    "Level 2-1": GrappleDogItemData(code=201,type=ItemClassification.progression),
    "Level 2-2": GrappleDogItemData(code=202,type=ItemClassification.progression),
    "Level 2-3": GrappleDogItemData(code=203,type=ItemClassification.progression),
    "Level 2-4": GrappleDogItemData(code=204,type=ItemClassification.progression),
    "Level 2-5": GrappleDogItemData(code=205,type=ItemClassification.progression),
    "Level 2-B": GrappleDogItemData(code=206,type=ItemClassification.progression_skip_balancing, can_create=lambda world: world.options.boss_level_unlock > 0),
    "Bonus 2-1": GrappleDogItemData(code=211,type=ItemClassification.progression),
    "Bonus 2-2": GrappleDogItemData(code=212,type=ItemClassification.progression),
    "Bonus 2-3": GrappleDogItemData(code=213,type=ItemClassification.progression),
    "Bonus 2-4": GrappleDogItemData(code=214,type=ItemClassification.progression),
    
    "Level 3-1": GrappleDogItemData(code=301,type=ItemClassification.progression),
    "Level 3-2": GrappleDogItemData(code=302,type=ItemClassification.progression),
    "Level 3-3": GrappleDogItemData(code=303,type=ItemClassification.progression),
    "Level 3-4": GrappleDogItemData(code=304,type=ItemClassification.progression),
    "Level 3-5": GrappleDogItemData(code=305,type=ItemClassification.progression),
    "Level 3-B": GrappleDogItemData(code=306,type=ItemClassification.progression_skip_balancing, can_create=lambda world: world.options.boss_level_unlock > 0),
    "Bonus 3-1": GrappleDogItemData(code=311,type=ItemClassification.progression),
    "Bonus 3-2": GrappleDogItemData(code=312,type=ItemClassification.progression),
    "Bonus 3-3": GrappleDogItemData(code=313,type=ItemClassification.progression),
    "Bonus 3-4": GrappleDogItemData(code=314,type=ItemClassification.progression),
    
    "Level 4-1": GrappleDogItemData(code=401,type=ItemClassification.progression),
    "Level 4-2": GrappleDogItemData(code=402,type=ItemClassification.progression),
    "Level 4-3": GrappleDogItemData(code=403,type=ItemClassification.progression),
    "Level 4-4": GrappleDogItemData(code=404,type=ItemClassification.progression),
    "Level 4-5": GrappleDogItemData(code=405,type=ItemClassification.progression),
    "Level 4-B": GrappleDogItemData(code=406,type=ItemClassification.progression_skip_balancing, can_create=lambda world: world.options.boss_level_unlock > 0),
    "Bonus 4-1": GrappleDogItemData(code=411,type=ItemClassification.progression),
    "Bonus 4-2": GrappleDogItemData(code=412,type=ItemClassification.progression),
    "Bonus 4-3": GrappleDogItemData(code=413,type=ItemClassification.progression),
    "Bonus 4-4": GrappleDogItemData(code=414,type=ItemClassification.progression),
    
    "Level 5-1": GrappleDogItemData(code=501,type=ItemClassification.progression),
    "Level 5-2": GrappleDogItemData(code=502,type=ItemClassification.progression),
    "Level 5-3": GrappleDogItemData(code=503,type=ItemClassification.progression),
    "Level 5-4": GrappleDogItemData(code=504,type=ItemClassification.progression),
    "Level 5-5": GrappleDogItemData(code=505,type=ItemClassification.progression),
    "Level 5-B": GrappleDogItemData(code=506,type=ItemClassification.progression_skip_balancing, can_create=lambda world: world.options.boss_level_unlock > 0),
    "Bonus 5-1": GrappleDogItemData(code=511,type=ItemClassification.progression),
    "Bonus 5-2": GrappleDogItemData(code=512,type=ItemClassification.progression),
    "Bonus 5-3": GrappleDogItemData(code=513,type=ItemClassification.progression),
    "Bonus 5-4": GrappleDogItemData(code=514,type=ItemClassification.progression),
    
    "Level 6-1": GrappleDogItemData(code=601,type=ItemClassification.progression),
    "Level 6-2": GrappleDogItemData(code=602,type=ItemClassification.progression),
    "Level 6-3": GrappleDogItemData(code=603,type=ItemClassification.progression),
    "Bonus 6-1": GrappleDogItemData(code=611,type=ItemClassification.progression),
    "Bonus 6-2": GrappleDogItemData(code=612,type=ItemClassification.progression),
    "Bonus 6-3": GrappleDogItemData(code=613,type=ItemClassification.progression),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
