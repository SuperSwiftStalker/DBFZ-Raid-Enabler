"""Raid boss data and lookup functions."""

RAID_BOSSES = {
    1: "The Emperor Strikes Back",
    2: "The Cell Games Main Event",
    3: "The Might of a Majin",
    4: "Living Legend of Universe 6",
    5: "Universe 7's God of Destruction",
    6: "Ominous Android",
    7: "Leading the Pack",
    8: "Heated, Furious, Ultimate Battle",
    9: "Father of Goku",
    10: "Future Freedom Fighters",
    11: "Foes from a Fearsome Future",
    12: "Pushing Past the Limits",
    13: "Savage Saiyan Showdown",
    14: "Android Assault",
    15: "Cooler's Revenge",
    16: "Beyond the Gods",
    17: "Videl's Training",
    18: "Goku Gauntlet",
    19: "From the Depths of Hell",
    20: "The Ultimate Fusion",
    21: "Power Incarnate",
    22: "Defiant in the Face of Despair",
    23: "A God in Mortal Form",
    24: "Fusion is Child's Play!",
    25: "Defenders of the Future",
    26: "Warm-Hearted Warrior",
    27: "The Best of Universe 7",
    28: "A Once Fearsome Foe",
    29: "Float Like a Crane, Sting Like a... Turtle?",
    30: "Earth's Mightiest",
    31: "The Power of a God",
    32: "First in Female Fusion",
    33: "God Among Gods",
    34: "The Greatest Kamehameha",
    35: "Facing the Fusions",
    36: "Trouble with a Tuffle",
    37: "Elegant Androids",
    38: "Ultimate Zenkai Battle"
}


def get_raid_name(raid_index: int) -> str:
    """
    Get raid boss name by index.

    Args:
        raid_index: Raid number (1-38)

    Returns:
        Raid boss name or "Unknown Raid" if not found
    """
    return RAID_BOSSES.get(raid_index, f"Unknown Raid {raid_index}")


def get_all_raids() -> list[tuple[int, str]]:
    """
    Get all raids as (index, name) tuples for UI display.

    Returns:
        List of (index, name) tuples sorted by index
    """
    return [(idx, name) for idx, name in sorted(RAID_BOSSES.items())]


def is_valid_raid_index(raid_index: int) -> bool:
    """
    Check if raid index is valid.

    Args:
        raid_index: Raid number to validate

    Returns:
        True if valid (1-38), False otherwise
    """
    return raid_index in RAID_BOSSES
