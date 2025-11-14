#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import os
import sys
import textwrap
import time
import re

from data_tables import (
    RARITIES,
    ITEM_TYPES,
    MATERIALS,
    QUALITIES,
    ENCHANTMENTS,
    ORIGINS,
    QUIRKS,
    ATTUNEMENT_REQUIREMENTS,
    MECHANICAL_EFFECTS,
    THEMED_MECHANICAL_EFFECTS,
)

# ==========================
#   ANSI COLOR DEFINITIONS
# ==========================

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

# Basic colors
BLACK   = "\033[30m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"

# Bright
BRIGHT_BLACK   = "\033[90m"
BRIGHT_RED     = "\033[91m"
BRIGHT_GREEN   = "\033[92m"
BRIGHT_YELLOW  = "\033[93m"
BRIGHT_BLUE    = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN    = "\033[96m"
BRIGHT_WHITE   = "\033[97m"

# Backgrounds
BG_BLACK   = "\033[40m"
BG_RED     = "\033[41m"
BG_GREEN   = "\033[42m"
BG_YELLOW  = "\033[43m"
BG_BLUE    = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN    = "\033[46m"
BG_WHITE   = "\033[47m"

BG_BRIGHT_BLACK   = "\033[100m"
BG_BRIGHT_RED     = "\033[101m"
BG_BRIGHT_GREEN   = "\033[102m"
BG_BRIGHT_YELLOW  = "\033[103m"
BG_BRIGHT_BLUE    = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN    = "\033[106m"
BG_BRIGHT_WHITE   = "\033[107m"


def color(text, *styles):
    """Apply one or more ANSI styles to text."""
    return "".join(styles) + str(text) + RESET


ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(s: str) -> str:
    """Remove ANSI escape sequences for width calculations."""
    return ANSI_ESCAPE_RE.sub("", s)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# ==========================
#   RARITY STYLES
# ==========================

RARITY_STYLES = {
    "Common":    {"color": BRIGHT_BLACK,   "emoji": "⚪"},
    "Uncommon":  {"color": BRIGHT_GREEN,   "emoji": "🟢"},
    "Rare":      {"color": BRIGHT_BLUE,    "emoji": "🔵"},
    "Very Rare": {"color": BRIGHT_MAGENTA, "emoji": "🟣"},
    "Legendary": {"color": BRIGHT_YELLOW,  "emoji": "🟡"},
    "Artifact":  {"color": BRIGHT_RED,     "emoji": "🔴"},
}


# ==========================
#   DISPLAY HELPERS
# ==========================

def gradient_title(text):
    """Apply a simple color gradient across the title text."""
    gradient_colors = [
        BRIGHT_MAGENTA,
        BRIGHT_BLUE,
        BRIGHT_CYAN,
        BRIGHT_GREEN,
        BRIGHT_YELLOW,
        BRIGHT_RED,
    ]
    colored_chars = []
    for i, ch in enumerate(text):
        c = gradient_colors[i % len(gradient_colors)]
        colored_chars.append(color(ch, BOLD, c))
    return "".join(colored_chars)


def print_banner():
    title = "⚔️ ARCANE ARMORY ⚔️"
    subtitle = "🎲 A Tiny D&D Fantasy Item Forge 🎲"

    print()
    print(" " * 4 + gradient_title(title))
    print(" " * 4 + color("═" * len(title), BRIGHT_BLACK))
    print()
    print(" " * 2 + color(subtitle, BRIGHT_CYAN, BOLD))
    print(" " * 2 + color("Press [Enter] to forge an item, or type 'q' to quit.", BRIGHT_BLACK))
    print()


def build_item_name(rarity_name, material, quality, item_type):
    if random.random() < 0.4:
        # Named artifact style
        epithets = [
            "the Dragonsong",
            "the Starforged",
            "the Umbral Edge",
            "the Dawnbreaker",
            "the Soulbound",
            "the Dreamweaver",
            "the Gravewhisper",
            "the Stormcall",
            "the Night's Embrace",
            "the Sunshard",
            "the Last Oath",
            "the Silent Choir",
        ]
        epithet = random.choice(epithets)
        base = f"{quality.title()} {item_type.title()}"
        return f"{base} of {epithet}"
    else:
        return f"{rarity_name} {quality} {material} {item_type}"


def infer_theme(material, quality, enchantment):
    """Infer a loose 'theme' (fire, cold, shadow, etc.) from the item's flavor text."""
    text = " ".join(
        [
            material or "",
            quality or "",
            enchantment or "",
        ]
    ).lower()

    if any(w in text for w in ("flame", "fire", "ember", "ash", "inferno", "lava", "scorch", "burn", "sun")):
        return "fire"
    if any(w in text for w in ("frost", "ice", "icy", "cold", "winter", "snow")):
        return "cold"
    if any(w in text for w in ("shadow", "night", "dark", "gloom", "umbral", "void", "shade", "ghost", "spectral")):
        return "shadow"
    if any(w in text for w in ("storm", "lightning", "thunder", "tempest", "squall")):
        return "storm"
    if any(w in text for w in ("vine", "root", "moss", "leaf", "petal", "forest", "druid", "beast", "animal", "nature", "wood", "fey")):
        return "fey"
    if any(w in text for w in ("holy", "divine", "radiant", "saint", "angel", "celestial", "blessed", "hallowed")):
        return "radiant"
    if any(w in text for w in ("blood", "bone", "grave", "death", "corpse", "skull", "necrotic", "wither")):
        return "necrotic"
    if any(w in text for w in ("arcane", "spell", "wizard", "mage", "rune", "sigil", "glyph", "scroll", "tome")):
        return "arcane"
    return "generic"


def pick_mechanical_effect(material, quality, enchantment):
    """Pick a mechanical effect, preferring theme-matched entries if available."""
    theme = infer_theme(material, quality, enchantment)
    themed_pool = THEMED_MECHANICAL_EFFECTS.get(theme, [])
    if themed_pool:
        return random.choice(themed_pool)
    # Fallback to the generic pool if no themed effects are available
    return random.choice(MECHANICAL_EFFECTS)


def generate_item():
    rarity_name = random.choice(RARITIES)
    rarity_style = RARITY_STYLES.get(
        rarity_name, {"color": BRIGHT_WHITE, "emoji": "✨"}
    )
    rarity_color = rarity_style["color"]
    rarity_emoji = rarity_style["emoji"]

    item_type = random.choice(ITEM_TYPES)
    material = random.choice(MATERIALS)
    quality = random.choice(QUALITIES)
    enchantment = random.choice(ENCHANTMENTS)
    origin = random.choice(ORIGINS)
    quirk = random.choice(QUIRKS)
    attune = random.choice(ATTUNEMENT_REQUIREMENTS)
    effect = pick_mechanical_effect(material, quality, enchantment)

    name = build_item_name(rarity_name, material, quality, item_type)

    return {
        "name": name,
        "rarity_name": rarity_name,
        "rarity_color": rarity_color,
        "rarity_emoji": rarity_emoji,
        "type": item_type,
        "material": material,
        "quality": quality,
        "enchantment": enchantment,
        "origin": origin,
        "quirk": quirk,
        "attune": attune,
        "effect": effect,
    }


def framed_block(lines, border_color=BRIGHT_BLUE):
    """Return a list of strings forming a nice framed box around the given lines."""
    # Compute width based on visible characters only (ignore ANSI color codes)
    width = max(len(strip_ansi(line)) for line in lines)
    top = color("┌" + "─" * (width + 2) + "┐", border_color)
    bottom = color("└" + "─" * (width + 2) + "┘", border_color)
    framed = [top]
    for line in lines:
        visible_width = len(strip_ansi(line))
        pad = " " * (width - visible_width)
        framed.append(color("│ ", border_color) + line + pad + " " + color("│", border_color))
    framed.append(bottom)
    return framed


def render_item_card(item):
    rarity_str = f"{item['rarity_emoji']} {item['rarity_name']}"
    rarity_str_colored = color(rarity_str, item["rarity_color"], BOLD)
    name_str = color(item["name"], BRIGHT_YELLOW, BOLD)

    type_line = color("Type: ", BRIGHT_CYAN, BOLD) + f"{item['quality']} {item['material']} {item['type']}"
    rarity_line = color("Rarity: ", BRIGHT_CYAN, BOLD) + rarity_str_colored

    mech_line = color("Mechanic: ", BRIGHT_CYAN, BOLD) + item["effect"]
    attune_line = color("Attunement: ", BRIGHT_CYAN, BOLD) + item["attune"]

    # Wrap longer text sections
    wrapper = textwrap.TextWrapper(width=70)

    lore_lines = wrapper.wrap(
        f"Forged origin: {item['origin']}. Its magic is such that {item['enchantment']}."
    )
    quirk_lines = wrapper.wrap(f"Quirk: {item['quirk']}.")

    body = [
        name_str,
        rarity_line,
        type_line,
        "",
        mech_line,
        attune_line,
        "",
    ]
    body.append(color("📜 Lore:", BRIGHT_MAGENTA, BOLD))
    body.extend(lore_lines)
    body.append("")
    body.append(color("✨ Oddities:", BRIGHT_MAGENTA, BOLD))
    body.extend(quirk_lines)

    return framed_block(body, border_color=BRIGHT_BLUE)


def slow_print(lines, delay=0.01):
    """Print lines with a subtle scrolling effect."""
    for line in lines:
        print(line)
        time.sleep(delay)


def main():
    clear_screen()
    print_banner()

    while True:
        user_input = input(
            color("✨ [Enter] forge item  |  'q' quit > ", BRIGHT_GREEN, BOLD)
        )
        if user_input.strip().lower().startswith("q"):
            print(color("May your loot be ever shiny. Farewell! 🪙✨", BRIGHT_CYAN))
            break

        clear_screen()
        print_banner()
        item = generate_item()
        card = render_item_card(item)
        slow_print(card, delay=0.004)
        print()
        print(
            color("💡 Tip:", BRIGHT_BLACK, BOLD),
            color("Use this as inspiration; tweak stats to fit your table.", BRIGHT_BLACK),
        )
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(color("Interrupted by user. May your dice roll high! 🎲", BRIGHT_CYAN))
