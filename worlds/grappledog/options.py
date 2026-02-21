from dataclasses import dataclass
from Options import Choice, OptionGroup, Range, Toggle,DefaultOnToggle, PerGameCommonOptions

class Goal(Choice):
    """How to win the game"""
    display_name = "Goal"
    default = 0
    option_defeat_nul = 0
    #option_beat_all_levels = 1
    #option_all_gems = 2
    #option_one_hundred_percent = 3
    
class CheckBanking(Choice):
    """When do checks get sent"""
    display_name = "Check Banking"
    default = 0
    option_instant = 0
    #option_checkpoint = 1
    #option_level_complete = 2
    
class RandomiseGadgets(Toggle):
    """Whether to add gadgets to the item pool vs beating bosses"""
    display_name = "Randomise Gadgets"

class StartingLevels(Range):
    """How many levels are available at the start of the game"""
    display_name = "Starting Levels"
    range_start = 0
    default = 1
    range_end = 56
    
class LevelProgression(Choice):
    """WIP: Not Yet Implemented"""
    display_name = "WIP: Level Progression"
    default = 0
    option_fully_random = 0
    
class StartWithHook(DefaultOnToggle):
    """Whether you start with the hook"""
    display_name = "Start With Hook"

class MovementRando(Toggle):
    """Whether movement abilities start locked"""
    display_name = "Movement Rando"

class UnlockableDoubleJump(Toggle):
    """WIP: Not Yet Implemented   
        Whether a Double Jump item gets added to the pool"""
    display_name = "WIP: Add Double Jump"
    
class DoubleJumpRefresh(Choice):
    """WIP: Not Yet Implemented   
    If double jump is enabled, when does it refresh"""
    display_name = "WIP: Double Jump Refresh"
    default = 0
    option_on_ground = 0
    option_wall_jump = 1
    option_grapple = 2
    option_bounce = 3
    option_progressive = 4

class StartingHealth(Range):
    """How much health you start with."""
    display_name = "Starting Health"
    range_start = 1
    default = 4
    range_end = 8
    
class MaxHealth(Range):
    """How much health you start with."""
    display_name = "Max Health"
    range_start = 1
    default = 4
    range_end = 8
    
class MinimumGemsInPool(Range):
    """How much health you start with."""
    display_name = "Minimum Gems in Pool"
    range_start = 0
    default = 190
    range_end = 300
    
class RemainingGemUsefulness(Range):
    """WIP: Not Yet Implemented   
    What percentage of the remaining gems will be marked as useful as opposed to filler"""
    display_name = "WIP: Remaining Gem Usefulness"
    range_start = 0
    default = 40
    range_end = 100
    
class FruitGemOneTarget(Range):
    """How many fruit you need to get the first fruit gem"""
    display_name = "Fruit Gem 1 Target"
    range_start = 1
    default = 110
    range_end = 250
    
class FruitGemTwoTarget(Range):
    """How many fruit you need to get the second fruit gem"""
    display_name = "Fruit Gem 2 Target"
    range_start = 1
    default = 220
    range_end = 250
    
# Misc

class BoomerangScoreOne(Range):
    """What score is needed for Boomerang Bandit check 1. (0 disables the check)"""
    display_name = "Boomerang Bandit Score 1"
    range_start = 0
    default = 10000
    range_end = 999999
    
class BoomerangScoreTwo(Range):
    """What score is needed for Boomerang Bandit check 2. (0 disables the check)"""
    display_name = "Boomerang Bandit Score 3"
    range_start = 0
    default = 20000
    range_end = 999999
    
class BoomerangScoreThree(Range):
    """What score is needed for Boomerang Bandit check 3. (0 disables the check)"""
    display_name = "Boomerang Bandit Score 4"
    range_start = 0
    default = 30000
    range_end = 999999

class SpeedrunnerChoiceMultiplier(Range):
    """How many times more levels are required for speedrunner checks to be in logic"""
    display_name = "Speedrunner Choice Multiplier"
    range_start = 0 
    default = 3
    range_end = 5
    
class SpeedrunnerCountOne(Range):
    """How many gold medals are required for the speedrunner check. (0 disables the check)"""
    display_name = "Speedrunner Golds Required"
    range_start = 0 
    default = 1
    range_end = 33
class SpeedrunnerCountTwo(Range):
    """How many gold medals are required for the speedrunner check. (0 disables the check)"""
    display_name = "Speedrunner Golds Required"
    range_start = 0 
    default = 2
    range_end = 33
class SpeedrunnerCountThree(Range):
    """How many gold medals are required for the speedrunner check. (0 disables the check)"""
    display_name = "Speedrunner Golds Required"
    range_start = 0 
    default = 3
    range_end = 33

# Bosses

class BossLevelUnlock(Choice):
    """How you unlock boss levels"""
    display_name = "Boss Level Unlock Condition"
    default = 1
    option_gems = 0
    option_gems_and_level = 1
    option_level = 2
    
class GemsForBossOne(Range):
    """How many gems are needed to play level 1-B"""
    display_name = "Boss 1 Gems Needed"
    range_start = 0
    default = 25
    range_end = 300
    
class GemsForBossTwo(Range):
    """How many gems are needed to play level 2-B"""
    display_name = "Boss 2 Gems Needed"
    range_start = 0
    default = 40
    range_end = 300
    
class GemsForBossThree(Range):
    """How many gems are needed to play level 3-B"""
    display_name = "Boss 3 Gems Needed"
    range_start = 0
    default = 80
    range_end = 300
    
class GemsForBossFour(Range):
    """How many gems are needed to play level 4-B"""
    display_name = "Boss 4 Gems Needed"
    range_start = 0
    default = 120
    range_end = 300
    
class GemsForBossFive(Range):
    """How many gems are needed to play level 5-B"""
    display_name = "Boss 5 Gems Needed"
    range_start = 0
    default = 190
    range_end = 300
    
class RequireGadgetsForFinalBoss(DefaultOnToggle):
    """Whether the 4 gadgets are required to play level 5-B"""
    display_name = "Require Gadgets for Final Boss"
    
@dataclass
class GrappleDogOptions(PerGameCommonOptions):
    # Game Conditions
    goal: Goal
    check_banking: CheckBanking
    randomise_gadgets: RandomiseGadgets
    # unlockable_double_jump: UnlockableDoubleJump
    # double_jump_refresh: DoubleJumpRefresh
    start_with_hook: StartWithHook
    movement_rando: MovementRando
    starting_levels: StartingLevels
    starting_health: StartingHealth
    max_health: MaxHealth
    level_progression: LevelProgression
    
    minimum_gems_in_pool: MinimumGemsInPool
    remaining_gem_usefulness: RemainingGemUsefulness
    fruit_gem_one_target: FruitGemOneTarget
    fruit_gem_two_target: FruitGemTwoTarget
    speedrunner_choice_multiplier: SpeedrunnerChoiceMultiplier
    speedrunner_count_one: SpeedrunnerCountOne
    speedrunner_count_two: SpeedrunnerCountTwo
    speedrunner_count_three: SpeedrunnerCountThree
    # Misc
    boomerang_score_one: BoomerangScoreOne
    boomerang_score_two: BoomerangScoreTwo
    boomerang_score_three: BoomerangScoreThree
    # Bosses
    boss_level_unlock: BossLevelUnlock
    gems_for_boss_one: GemsForBossOne
    gems_for_boss_two: GemsForBossTwo
    gems_for_boss_three: GemsForBossThree
    gems_for_boss_four: GemsForBossFour
    gems_for_boss_five: GemsForBossFive
    require_gadgets_for_final_boss: RequireGadgetsForFinalBoss
    
option_groups = [
    OptionGroup("Goals", [
        Goal,
        RandomiseGadgets,
        LevelProgression,
        StartingLevels
    ]),
    OptionGroup("Abilities", [
        StartWithHook,
        MovementRando,
        StartingHealth,
        MaxHealth,
        UnlockableDoubleJump,
        DoubleJumpRefresh
    ]),
    OptionGroup("Checks", [
        CheckBanking,
        MinimumGemsInPool,
        RemainingGemUsefulness,
        FruitGemOneTarget,
        FruitGemTwoTarget,
        SpeedrunnerChoiceMultiplier,
        SpeedrunnerCountOne,
        SpeedrunnerCountTwo,
        SpeedrunnerCountThree
    ]),
    OptionGroup("Bosses", [
        BossLevelUnlock,
        GemsForBossOne,
        GemsForBossTwo,
        GemsForBossThree,
        GemsForBossFour,
        GemsForBossFive,
        RequireGadgetsForFinalBoss
    ]),
]

