#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data tables for the D&D fantasy item generator.
Feel free to expand these lists to flavor it for your own setting.
"""

# Rarity names (colors/emojis are handled in the main script)
RARITIES = [
    "Common",
    "Uncommon",
    "Rare",
    "Very Rare",
    "Legendary",
    "Artifact",
]

ITEM_TYPES = [
    "sword",
    "dagger",
    "greatsword",
    "longbow",
    "shortbow",
    "warhammer",
    "battleaxe",
    "mace",
    "staff",
    "wand",
    "orb",
    "shield",
    "breastplate",
    "leather armor",
    "cloak",
    "ring",
    "amulet",
    "belt",
    "boots",
    "helm",
    "gauntlets",
    "tome",
    "instrument",
    "lantern",
    # +5 extra types
    "maul",
    "flail",
    "chakram",
    "crossbow",
    "spellbook",
]

MATERIALS = [
    "iron",
    "steel",
    "obsidian",
    "mithral",
    "adamantine",
    "dragonbone",
    "cold iron",
    "star metal",
    "shadowglass",
    "crystalline",
    "runic stone",
    "ghostwood",
    "moonsteel",
    # +5 extra materials
    "bloodstone",
    "void crystal",
    "sunforged bronze",
    "eldritch ivory",
    "wyrmscale",
]

QUALITIES = [
    "ornate",
    "runed",
    "weathered",
    "gleaming",
    "ancient",
    "ceremonial",
    "barbaric",
    "elegant",
    "jagged",
    "etched",
    "sunglow",
    "frostbitten",
    "ember-forged",
    # +5 extra qualities
    "saintly",
    "cursed",
    "prismatic",
    "mirrorbright",
    "rootbound",
]

ENCHANTMENTS = [
    "flames dance along its edge 🔥",
    "it hums softly when danger is near",
    "it whispers the names of the dead in a chilling murmur 💀",
    "it glows faintly under the light of the moon 🌙",
    "its surface drinks in surrounding light",
    "it sings in battle with eerie harmony",
    "it bends shadows around the wielder",
    "it crackles with latent storm energy ⚡",
    "it radiates a soothing warmth",
    "it leaves faint spectral afterimages when swung",
    # +5 extra enchantments
    "tiny motes of starlight drift from it when drawn ✨",
    "a faint chorus of distant voices echoes inside it",
    "it briefly reveals invisible runes on nearby surfaces",
    "it leaves behind the scent of rain on stone",
    "its reflection sometimes moves a heartbeat out of sync",
]

ORIGINS = [
    "forged in the heart of a dying star",
    "crafted by a forgotten archmage",
    "recovered from the depths of an ancient ruin",
    "woven from the dreams of sleeping gods",
    "hammered on an anvil of dragonfire",
    "blessed in the waters of a sacred spring",
    "stolen from the hoard of a jealous demon",
    "found in the shattered vaults beneath a ruined city",
    "gifted by the fey courts at a terrible price",
    "salvaged from the armor of a fallen celestial",
    # +5 extra origins
    "pieced together from relics scattered across a dozen battlefields",
    "sung into being by a circle of druids at solstice",
    "excavated from a meteorite that never cooled",
    "traded for a single whispered secret in a midnight market",
    "recovered from a time-locked vault that should never have opened",
]

QUIRKS = [
    "occasionally changes weight at random",
    "emits the scent of ozone when used",
    "causes faint spectral motes to orbit the wielder",
    "sometimes speaks in riddles only the wielder can hear",
    "is invisible to anyone who has lied in the last hour",
    "refuses to be drawn against the innocent",
    "leaves footprints of light wherever it goes",
    "causes nearby candles to burn with colored flames 🕯️",
    "slowly repairs itself from any damage",
    "seems slightly heavier in the presence of dragons 🐉",
    # +5 extra quirks
    "occasionally giggles softly when no one is looking",
    "casts a shadow that sometimes points in the wrong direction",
    "rings like crystal when lies are spoken nearby",
    "attracts small harmless animals that refuse to leave",
    "its reflection is always a little older than reality",
]

ATTUNEMENT_REQUIREMENTS = [
    "Attunement required by a spellcaster",
    "Attunement required by a creature of good alignment",
    "Attunement required by a creature of non‑lawful alignment",
    "Attunement required by a proficient martial weapon user",
    "No attunement required",
    # +5 extra requirements
    "Attunement required by a creature who has slain a dragon",
    "Attunement required by a creature proficient with heavy armor",
    "Attunement required by a bard, cleric, or paladin",
    "Attunement required by a creature who has made a pact with a patron",
    "Attunement required by a creature bearing a notable scar",
]

MECHANICAL_EFFECTS = [
    "+1 bonus to attack and damage rolls",
    "+2 bonus to AC while worn",
    "advantage on saving throws against being charmed",
    "resistance to fire damage",
    "resistance to cold damage",
    "resistance to necrotic damage",
    "you can cast Detect Magic at will",
    "you can cast Misty Step once per short rest",
    "you can speak, read, and write Draconic",
    "once per day, you can reroll a failed attack roll",
    "your walking speed increases by 10 ft.",
    # +5 extra effects
    "you gain darkvision out to 60 ft.",
    "once per long rest, you can turn invisible for 1 minute",
    "you have advantage on Initiative rolls",
    "you can breathe underwater",
    "your spell save DC for one class increases by 1",
]
