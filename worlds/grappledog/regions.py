from typing import Callable, Dict, List, NamedTuple
from BaseClasses import CollectionState


class GrappleDogRegionData(NamedTuple):
    connecting_regions: List[str] = []
    rules: Dict[str, Callable[[CollectionState], bool]] = None

region_data_table: Dict[str, GrappleDogRegionData] = {
    "Menu": GrappleDogRegionData(["Game"]),
    "Game": GrappleDogRegionData(["World 1", "World 2", "World 3", "World 4", "World 5", "World 6"]),
    
    "World 1": GrappleDogRegionData(["Level 1-1", "Level 1-2", "Level 1-3", "Level 1-4", "Level 1-5", "Level 1-B", "Bonus 1-1", "Bonus 1-2", "Bonus 1-3", "Bonus 1-4"]),
    "Level 1-1": GrappleDogRegionData(),
    "Level 1-2": GrappleDogRegionData(),
    "Level 1-3": GrappleDogRegionData(),
    "Level 1-4": GrappleDogRegionData(),
    "Level 1-5": GrappleDogRegionData(),
    "Level 1-B": GrappleDogRegionData(),
    "Bonus 1-1": GrappleDogRegionData(),
    "Bonus 1-2": GrappleDogRegionData(),
    "Bonus 1-3": GrappleDogRegionData(),
    "Bonus 1-4": GrappleDogRegionData(),
    
    "World 2": GrappleDogRegionData(["Level 2-1", "Level 2-2", "Level 2-3", "Level 2-4", "Level 2-5", "Level 2-B", "Bonus 2-1", "Bonus 2-2", "Bonus 2-3", "Bonus 2-4"]),
    "Level 2-1": GrappleDogRegionData(),
    "Level 2-2": GrappleDogRegionData(),
    "Level 2-3": GrappleDogRegionData(),
    "Level 2-4": GrappleDogRegionData(),
    "Level 2-5": GrappleDogRegionData(),
    "Level 2-B": GrappleDogRegionData(),
    "Bonus 2-1": GrappleDogRegionData(),
    "Bonus 2-2": GrappleDogRegionData(),
    "Bonus 2-3": GrappleDogRegionData(),
    "Bonus 2-4": GrappleDogRegionData(),
    
    "World 3": GrappleDogRegionData(["Level 3-1", "Level 3-2", "Level 3-3", "Level 3-4", "Level 3-5", "Level 3-B", "Bonus 3-1", "Bonus 3-2", "Bonus 3-3", "Bonus 3-4"]),
    "Level 3-1": GrappleDogRegionData(),
    "Level 3-2": GrappleDogRegionData(),
    "Level 3-3": GrappleDogRegionData(),
    "Level 3-4": GrappleDogRegionData(),
    "Level 3-5": GrappleDogRegionData(),
    "Level 3-B": GrappleDogRegionData(),
    "Bonus 3-1": GrappleDogRegionData(),
    "Bonus 3-2": GrappleDogRegionData(),
    "Bonus 3-3": GrappleDogRegionData(),
    "Bonus 3-4": GrappleDogRegionData(),
    
    "World 4": GrappleDogRegionData(["Level 4-1", "Level 4-2", "Level 4-3", "Level 4-4", "Level 4-5", "Level 4-B", "Bonus 4-1", "Bonus 4-2", "Bonus 4-3", "Bonus 4-4"]),
    "Level 4-1": GrappleDogRegionData(),
    "Level 4-2": GrappleDogRegionData(),
    "Level 4-3": GrappleDogRegionData(),
    "Level 4-4": GrappleDogRegionData(),
    "Level 4-5": GrappleDogRegionData(),
    "Level 4-B": GrappleDogRegionData(),
    "Bonus 4-1": GrappleDogRegionData(),
    "Bonus 4-2": GrappleDogRegionData(),
    "Bonus 4-3": GrappleDogRegionData(),
    "Bonus 4-4": GrappleDogRegionData(),
    
    "World 5": GrappleDogRegionData(["Level 5-1", "Level 5-2", "Level 5-3", "Level 5-4", "Level 5-5", "Level 5-B", "Bonus 5-1", "Bonus 5-2", "Bonus 5-3", "Bonus 5-4"]),
    "Level 5-1": GrappleDogRegionData(),
    "Level 5-2": GrappleDogRegionData(),
    "Level 5-3": GrappleDogRegionData(),
    "Level 5-4": GrappleDogRegionData(),
    "Level 5-5": GrappleDogRegionData(),
    "Level 5-B": GrappleDogRegionData(),
    "Bonus 5-1": GrappleDogRegionData(),
    "Bonus 5-2": GrappleDogRegionData(),
    "Bonus 5-3": GrappleDogRegionData(),
    "Bonus 5-4": GrappleDogRegionData(),
    
    "World 6": GrappleDogRegionData(["Level 6-1", "Level 6-2", "Level 6-3", "Bonus 6-1", "Bonus 6-2", "Bonus 6-3"]),
    "Level 6-1": GrappleDogRegionData(),
    "Level 6-2": GrappleDogRegionData(),
    "Level 6-3": GrappleDogRegionData(),
    "Bonus 6-1": GrappleDogRegionData(),
    "Bonus 6-2": GrappleDogRegionData(),
    "Bonus 6-3": GrappleDogRegionData(),
}
