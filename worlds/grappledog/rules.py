import os
import json
from typing import TYPE_CHECKING
from BaseClasses import LocationProgressType
from worlds.generic.Rules import set_rule
# from rules import True_, False_, Has

if TYPE_CHECKING:
    from . import GrappleDogWorld
    
with open(os.path.join(os.path.dirname(__file__), 'fruit_rules.json'), 'r') as file:
    fruit_rules = json.load(file)

# ----------------------------
# Boolean Requirement Compiler
# ----------------------------

# def build_rule(expr: str):
#     """
#     Converts a string like:
#         "Grapple + Bounce Pads + Wall Jump || Balloons"
#     Into a composed Rule object using:
#         +   => And (&)
#         ||  => Or (|)
#     """

#     expr = expr.strip()

#     if not expr:
#         return True_()

#     # Split on AND first
#     and_segments = [segment.strip() for segment in expr.split("+")]

#     and_rules = []

#     for segment in and_segments:
#         # Split each AND segment into OR parts
#         or_tokens = [token.strip() for token in segment.split("||")]

#         if len(or_tokens) == 1:
#             # Single token
#             and_rules.append(Has(or_tokens[0]))
#         else:
#             # Build OR rule
#             or_rule = Has(or_tokens[0])
#             for token in or_tokens[1:]:
#                 or_rule = or_rule | Has(token)
#             and_rules.append(or_rule)

#     # Combine all AND rules
#     if not and_rules:
#         return True_()

#     rule = and_rules[0]
#     for r in and_rules[1:]:
#         rule = rule & r

#     return rule

    
def requirement_is_met(expr, available):
    # OR takes precedence over AND
    and_groups = [group.strip() for group in expr.split("+")]

    for group in and_groups:
        or_parts = [part.strip() for part in group.split("||")]

        if not any(part in available for part in or_parts):
            return False

    return True


def collect_requirement_tokens(obj, tokens):
    """
    Recursively collect all ability names used in requirement keys.
    """
    for key, value in obj.items():
        if key != "":
            parts = key.replace("+", "||").split("||")
            for part in parts:
                tokens.add(part.strip())

            collect_requirement_tokens(value, tokens)


def check_fruit(state):
    total = 0

    def traverse(obj, available):
        nonlocal total

        for key, value in obj.items():
            if key == "":
                total += value
            elif requirement_is_met(key, available):
                traverse(value, available)

    for level in fruit_rules.values():

        # 🔹 Collect all abilities referenced in this level
        tokens = set()
        collect_requirement_tokens(level, tokens)

        # 🔹 Ask state about each ability exactly once
        available = {
            ability for ability in tokens if state.has(ability)
        }

        traverse(level, available)

    return total
    
def check_fruit_for_level(state, level, player):
    total = 0

    def traverse(obj, available):
        nonlocal total

        for key, value in obj.items():
            if key == "":
                total += value
            elif requirement_is_met(key, available):
                traverse(value, available)

    level_data = fruit_rules[level]

        # 🔹 Collect all abilities referenced in this level
    tokens = set()
    collect_requirement_tokens(level_data, tokens)

    # 🔹 Ask state about each ability exactly once
    available = {
        ability for ability in tokens if state.has(ability, player)
    }

    traverse(level_data, available)

    return total
    

def can_collect(level_name, targets, state):
    level = fruit_rules.get(level_name)
    if not level:
        return [False] * len(targets)

    # Collect ability tokens used in this level
    tokens = set()
    collect_requirement_tokens(level, tokens)

    # Ask state once per ability
    available = {ability for ability in tokens if state.has(ability)}

    # Sort targets with original indices
    indexed_targets = sorted(
        enumerate(targets),
        key=lambda x: x[1]
    )

    results = [False] * len(targets)
    total = 0
    target_index = 0

    def traverse(obj):
        nonlocal total, target_index

        for key, value in obj.items():
            if key == "":
                total += value

                # Check thresholds in ascending order
                while (
                    target_index < len(indexed_targets)
                    and total >= indexed_targets[target_index][1]
                ):
                    original_index = indexed_targets[target_index][0]
                    results[original_index] = True
                    target_index += 1

                # Early exit if all targets satisfied
                if target_index >= len(indexed_targets):
                    return True

            elif requirement_is_met(key, available):
                if traverse(value):
                    return True

        return False

    traverse(level)

    return results


def evaluate_requirement(expr: str, state, player) -> bool:
    # Split on AND first
    and_parts = [part.strip() for part in expr.split("+")]

    # Each AND part may contain ORs
    outcome = True
    for part in and_parts:
        or_parts = [p.strip() for p in part.split("||")]
        if(len(or_parts) > 1):
            part_outcome = False
            for or_part in or_parts:
                part_outcome = part_outcome | state.has(or_part, player)
            outcome = outcome & part_outcome
        else:
            outcome = outcome & state.has(part, player)
    return outcome


def compile_requirement(expr: str):
    """
    Compiles a boolean requirement expression into a callable.
    
    Grammar:
        +   => AND
        ||  => OR
    
    Splits on + first, then || inside each segment.
    """
    and_groups = [
        [token.strip() for token in part.split("||")]
        for part in (segment.strip() for segment in expr.split("+"))
    ]

    def requirement(state, player):
        for or_group in and_groups:
            print(or_group)
            if not any(state.has(token, player) for token in or_group):
                return False
            
        return True

    return requirement


def compile_rules(lines):
    """
    Takes an array of strings like:
        "Grapple + Wall Jump - 5"
    and returns compiled (callable, value) pairs.
    """
    compiled = []

    for line in lines:
        try:
            expr, value = line.rsplit(" - ", 1)
        except ValueError:
            continue  # skip malformed lines

        requirement_fn = compile_requirement(expr.strip())
        compiled.append((requirement_fn, int(value.strip())))

    return compiled


def sum_matching_compiled(compiled_rules, state):
    """
    Evaluates compiled rules against a state and
    returns the sum of matching values.
    """
    total = 0
    for requirement_fn, value in compiled_rules:
        if requirement_fn(state):
            total += value
    return total


# ----------------------------
# Example Usage
# ----------------------------

# class State:
#     def __init__(self, abilities):
#         self.abilities = set(abilities)

#     def has(self, name):
#         return name in self.abilities


# if __name__ == "__main__":
#     lines = [
#         "Grapple + Wall Jump - 5",
#         "Balloons || Glide - 3",
#         "Grapple + Wall Jump - 2",
#     ]

#     # Compile once
#     compiled_rules = compile_rules(lines)

#     # Evaluate with a state
#     state = State(["Grapple", "Wall Jump"])

#     total = sum_matching_compiled(compiled_rules, state)

#     print("Total:", total)


# OR ==============

# requirement = compile_requirement(
#     "Grapple + Bounce Pads + Wall Jump || Balloons"
# )

# print(requirement(state, player))
    
def create_rules(world: "GrappleDogWorld"): 
    def boss_level_requirements_met(state, player, world_number, options):
        level_needed_acquired = True
        gem_count_needed = 0
        has_gadgets_needed = True
        match world_number:
            case 1:
                if (options.boss_level_unlock.value >= 1):
                    level_needed_acquired = state.has("Level 1-B", player)
                if (options.boss_level_unlock.value <= 1):
                    gem_count_needed = options.gems_for_boss_one
            case 2:
                if (options.boss_level_unlock.value >= 1):
                    level_needed_acquired = state.has("Level 2-B", player)
                if (options.boss_level_unlock.value <= 1):
                    gem_count_needed = options.gems_for_boss_two
            case 3:
                if (options.boss_level_unlock.value >= 1):
                    level_needed_acquired = state.has("Level 3-B", player)
                if (options.boss_level_unlock.value <= 1):
                    gem_count_needed = options.gems_for_boss_three
            case 4:
                if (options.boss_level_unlock.value >= 1):
                    level_needed_acquired = state.has("Level 4-B", player)
                if (options.boss_level_unlock.value <= 1):
                    gem_count_needed = options.gems_for_boss_four
            case 5:
                if (options.boss_level_unlock.value >= 1):
                    level_needed_acquired = state.has("Level 5-B", player)
                if (options.boss_level_unlock.value <= 1):
                    gem_count_needed = options.gems_for_boss_five
                if(options.require_gadgets_for_final_boss):
                    # has_gadgets_needed = state.can_reach(world.get_region("Level 1-B"), player) and state.can_reach(world.get_region("Level 2-B"), player) and state.can_reach(world.get_region("Level 3-B"), player) and state.can_reach(world.get_region("Level 4-B"), player)
                    has_gadgets_needed = state.has("Gadget 1", player) & state.has("Gadget 2", player) & state.has("Gadget 3", player) & state.has("Gadget 4", player)

        return level_needed_acquired & has_gadgets_needed & state.has("Gem", player, gem_count_needed) 
        
    multiworld = world.multiworld
    player = world.player
    options = world.options
    if(world.options.speedrunner_count_one.value > 0):
        multiworld.get_location('Speedrun (1 Gold)', player).access_rule = lambda state, player=player, options=options: state.has_group("Levels", player, max(0, min(33, options.speedrunner_count_one.value * 3))) & evaluate_requirement("Grapple Hook + Bounce Pads + Balloons + Cannons + Wall Jump + Climb + Swim + Slam", state, player)
        
    if(world.options.speedrunner_count_two.value > 0):
        multiworld.get_location('Speedrun (2 Gold)', player).access_rule = lambda state, player=player, options=options: state.has_group("Levels", player, max(0, min(33, options.speedrunner_count_two.value * 3))) & evaluate_requirement("Grapple Hook + Bounce Pads + Balloons + Cannons + Wall Jump + Climb + Swim + Slam", state, player)
        
    if(world.options.speedrunner_count_three.value > 0):
        multiworld.get_location('Speedrun (3 Gold)', player).access_rule = lambda state, player=player, options=options: state.has_group("Levels", player, max(0, min(33, options.speedrunner_count_three.value * 3))) & evaluate_requirement("Grapple Hook + Bounce Pads + Balloons + Cannons + Wall Jump + Climb + Swim + Slam", state, player)

    multiworld.get_region("Menu", player).add_exits(['Game'])
    multiworld.get_region("Game", player).add_exits(
        [ "World 1", "World 2", "World 3", "World 4", "World 5", "World 6" ],
        {
            "World 1": lambda state, player=player: world.options.level_progression.value == 0 or state.has("World 1", player),
            "World 2": lambda state, player=player: world.options.level_progression.value == 0 or state.has("World 2", player),
            "World 3": lambda state, player=player: world.options.level_progression.value == 0 or state.has("World 3", player),
            "World 4": lambda state, player=player: world.options.level_progression.value == 0 or state.has("World 4", player),
            "World 5": lambda state, player=player: world.options.level_progression.value == 0 or state.has("World 5", player),
            "World 6": lambda state, player=player: world.options.level_progression.value == 0 or state.has("World 6", player)
        }
    )
    
    multiworld.get_region("World 1", player).add_exits(
        [ "Level 1-1", "Level 1-2" , "Level 1-3" , "Level 1-4" ,"Level 1-5" , "Level 1-B" , "Bonus 1-1" , "Bonus 1-2" , "Bonus 1-3" , "Bonus 1-4" ],
        {
            "Level 1-1": lambda state, player=player: state.has("Level 1-1", player),
            "Level 1-2": lambda state, player=player: state.has("Level 1-2", player),
            "Level 1-3": lambda state, player=player: state.has("Level 1-3", player),
            "Level 1-4": lambda state, player=player: state.has("Level 1-4", player),
            "Level 1-5": lambda state, player=player: state.has("Level 1-5", player),
            "Level 1-B": lambda state, player=player, options=options: boss_level_requirements_met(state, player, 1, options),
            "Bonus 1-1": lambda state, player=player: state.has("Bonus 1-1", player),
            "Bonus 1-2": lambda state, player=player: state.has("Bonus 1-2", player),
            "Bonus 1-3": lambda state, player=player: state.has("Bonus 1-3", player),
            "Bonus 1-4": lambda state, player=player: state.has("Bonus 1-4", player),
        }
    )
    
    multiworld.get_region("World 2", player).add_exits(
        [ "Level 2-1", "Level 2-2" , "Level 2-3" , "Level 2-4" ,"Level 2-5" , "Level 2-B" , "Bonus 2-1" , "Bonus 2-2" , "Bonus 2-3" , "Bonus 2-4"  ],
        {
            "Level 2-1": lambda state, player=player: state.has("Level 2-1", player),
            "Level 2-2": lambda state, player=player: state.has("Level 2-2", player),
            "Level 2-3": lambda state, player=player: state.has("Level 2-3", player),
            "Level 2-4": lambda state, player=player: state.has("Level 2-4", player),
            "Level 2-5": lambda state, player=player: state.has("Level 2-5", player),
            "Level 2-B": lambda state, player=player, options=options: boss_level_requirements_met(state, player, 2, options),
            "Bonus 2-1": lambda state, player=player: state.has("Bonus 2-1", player),
            "Bonus 2-2": lambda state, player=player: state.has("Bonus 2-2", player),
            "Bonus 2-3": lambda state, player=player: state.has("Bonus 2-3", player),
            "Bonus 2-4": lambda state, player=player: state.has("Bonus 2-4", player),
        }
    )
            
    multiworld.get_region("World 3", player).add_exits(
        [ "Level 3-1", "Level 3-2" , "Level 3-3" , "Level 3-4" ,"Level 3-5" , "Level 3-B" , "Bonus 3-1" , "Bonus 3-2" , "Bonus 3-3" , "Bonus 3-4"  ],
        {
            "Level 3-1": lambda state, player=player: state.has("Level 3-1", player),
            "Level 3-2": lambda state, player=player: state.has("Level 3-2", player),
            "Level 3-3": lambda state, player=player: state.has("Level 3-3", player),
            "Level 3-4": lambda state, player=player: state.has("Level 3-4", player),
            "Level 3-5": lambda state, player=player: state.has("Level 3-5", player),
            "Level 3-B": lambda state, player=player, options=options: boss_level_requirements_met(state, player, 3, options),
            "Bonus 3-1": lambda state, player=player: state.has("Bonus 3-1", player),
            "Bonus 3-2": lambda state, player=player: state.has("Bonus 3-2", player),
            "Bonus 3-3": lambda state, player=player: state.has("Bonus 3-3", player),
            "Bonus 3-4": lambda state, player=player: state.has("Bonus 3-4", player),
        }
    )
    
    multiworld.get_region("World 4", player).add_exits(
        [ "Level 4-1", "Level 4-2" , "Level 4-3" , "Level 4-4" ,"Level 4-5" , "Level 4-B" , "Bonus 4-1" , "Bonus 4-2" , "Bonus 4-3" , "Bonus 4-4"  ],
        {
            "Level 4-1": lambda state, player=player: state.has("Level 4-1", player),
            "Level 4-2": lambda state, player=player: state.has("Level 4-2", player),
            "Level 4-3": lambda state, player=player: state.has("Level 4-3", player),
            "Level 4-4": lambda state, player=player: state.has("Level 4-4", player),
            "Level 4-5": lambda state, player=player: state.has("Level 4-5", player),
            "Level 4-B": lambda state, player=player, options=options: boss_level_requirements_met(state, player, 4, options),
            "Bonus 4-1": lambda state, player=player: state.has("Bonus 4-1", player),
            "Bonus 4-2": lambda state, player=player: state.has("Bonus 4-2", player),
            "Bonus 4-3": lambda state, player=player: state.has("Bonus 4-3", player),
            "Bonus 4-4": lambda state, player=player: state.has("Bonus 4-4", player),
        }
    )
    
    multiworld.get_region("World 5", player).add_exits(
        [ "Level 5-1", "Level 5-2" , "Level 5-3" , "Level 5-4" ,"Level 5-5" , "Level 5-B" , "Bonus 5-1" , "Bonus 5-2" , "Bonus 5-3" , "Bonus 5-4"  ],
        {
            "Level 5-1": lambda state, player=player: state.has("Level 5-1", player),
            "Level 5-2": lambda state, player=player: state.has("Level 5-2", player),
            "Level 5-3": lambda state, player=player: state.has("Level 5-3", player),
            "Level 5-4": lambda state, player=player: state.has("Level 5-4", player),
            "Level 5-5": lambda state, player=player: state.has("Level 5-5", player),
            "Level 5-B": lambda state, player=player, options=options: boss_level_requirements_met(state, player, 5, options),
            "Bonus 5-1": lambda state, player=player: state.has("Bonus 5-1", player),
            "Bonus 5-2": lambda state, player=player: state.has("Bonus 5-2", player),
            "Bonus 5-3": lambda state, player=player: state.has("Bonus 5-3", player),
            "Bonus 5-4": lambda state, player=player: state.has("Bonus 5-4", player),
        }
    )
                    
    multiworld.get_region("World 6", player).add_exits(
        [ "Level 6-1", "Level 6-2" , "Level 6-3" , "Bonus 6-1" , "Bonus 6-2" , "Bonus 6-3" ],
        {
            "Level 6-1": lambda state, player=player: state.has("Level 6-1", player),
            "Level 6-2": lambda state, player=player: state.has("Level 6-2", player),
            "Level 6-3": lambda state, player=player: state.has("Level 6-3", player),
            "Bonus 6-1": lambda state, player=player: state.has("Bonus 6-1", player),
            "Bonus 6-2": lambda state, player=player: state.has("Bonus 6-2", player),
            "Bonus 6-3": lambda state, player=player: state.has("Bonus 6-3", player),
        }
    )

    world.multiworld.completion_condition[world.player] = lambda state, player=player: state.has("Kiss From Rabbit", player)
    
