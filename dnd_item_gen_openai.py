#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenAI-enhanced version of the D&D item generator.

- Builds a base item from local random tables.
- Asks OpenAI gpt-5.1 to elaborate vivid lore, quirks, and optional tweaks.
- Falls back gracefully if OPENAI_API_KEY or openai client is not available.

Usage:
    export OPENAI_API_KEY="sk-..."   # or set via your preferred method
    python dnd_item_gen_openai.py
"""

import os
import random
import re
import textwrap
import time
import json
import base64
import sys
import shutil
import subprocess

# Optional OpenAI client
try:
    from openai import OpenAI
    _OPENAI_CLIENT = OpenAI()
except Exception:
    _OPENAI_CLIENT = None

# Optional Pillow for local image resizing
try:
    from PIL import Image
except Exception:
    Image = None

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

# Backgrounds (kept for possible future use)
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
    title = "⚔️ ARCANE ARMORY (GPT-ENHANCED) ⚔️"
    subtitle = "🎲 D&D Item Forge + gpt-5.1 Lore Booster 🤖"

    print()
    print(" " * 2 + gradient_title(title))
    print(" " * 2 + color("═" * len(title), BRIGHT_BLACK))
    print()
    print(" " * 2 + color(subtitle, BRIGHT_CYAN, BOLD))
    print(" " * 2 + color("Press [Enter] to forge an item, or type 'q' to quit.", BRIGHT_BLACK))
    print(" " * 2 + color("Note: Set OPENAI_API_KEY for AI-enhanced lore.", BRIGHT_BLACK))
    print()


# ==========================
#   BASE ITEM GENERATION
# ==========================

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


def generate_base_item():
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
    effect = random.choice(MECHANICAL_EFFECTS)

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


# ==========================
#   OPENAI ENHANCEMENT
# ==========================

def enhance_with_openai(item):
    """
    Call OpenAI gpt-5.1 to elaborate the item.

    Returns (enhanced_item, note_string).
    The note_string is shown in the UI so you can see if enhancement ran.
    """
    if _OPENAI_CLIENT is None or not os.getenv("OPENAI_API_KEY"):
        return item, "🔒 OpenAI not configured; showing base generator output."

    # Compact JSON for prompt
    base_json = json.dumps(item, ensure_ascii=False)

    system_prompt = (
        "You are a seasoned Dungeons & Dragons item designer. "
        "Given a base magic item, you elaborate its lore and quirks in a vivid but table-usable way. "
        "Keep it roughly 5e balanced, grounded in fantasy tone (no modern tech), "
        "and avoid contradicting the core concept."
    )

    user_prompt = (
        "Here is a base item description as JSON:\n"
        f"{base_json}\n\n"
        "Task:\n"
        "- Enrich the lore into 2–4 sentences of evocative description.\n"
        "- Provide 1–2 quirky behaviors or narrative oddities.\n"
        "- Optionally refine the item name and mechanical effect to be a bit more flavorful, "
        "but keep them mechanically close to the original.\n\n"
        "Respond ONLY as a JSON object with keys:\n"
        "  name: string (final item name, can reuse the original)\n"
        "  enhanced_lore: string (2–4 sentences)\n"
        "  enhanced_quirk: string (1–2 sentences; can combine multiple quirks)\n"
        "  mechanical_note: string (short note about how to interpret or keep it balanced)\n"
        "No extra commentary, no markdown."
    )

    try:
        resp = _OPENAI_CLIENT.chat.completions.create(
            model="gpt-5.1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.9,
            max_completion_tokens=400,
        )
        content = resp.choices[0].message.content
        data = json.loads(content)

        # Merge into item
        item["name"] = data.get("name", item["name"])
        item["enhanced_lore"] = data.get("enhanced_lore")
        item["enhanced_quirk"] = data.get("enhanced_quirk")
        item["mechanical_note"] = data.get("mechanical_note")
        note = "🤖 gpt-5.1 enhancement applied."
        return item, note

    except Exception as e:
        # Fail gracefully and show the error message in a subtle way
        item.setdefault("mechanical_note", "")
        note = f"⚠️ OpenAI enhancement failed: {e}"
        return item, note


def generate_item_image(item):
    """
    Use gpt-image-1 to generate an illustration for the item.

    Returns (b64_png_or_none, status_message).
    """
    if _OPENAI_CLIENT is None or not os.getenv("OPENAI_API_KEY"):
        return None, "🖼️ OpenAI not configured; no image generated."

    # Short image prompt based on the item fields
    prompt = (
        "Fantasy illustration of a Dungeons & Dragons style magic item. "
        f"Item name: {item.get('name')}. "
        f"Rarity: {item.get('rarity_name')}. "
        f"Type: {item.get('quality')} {item.get('material')} {item.get('type')}. "
        "Show the item alone on a simple, dark backdrop, no text, no characters, "
        "in a painterly illustration style."
    )

    try:
        resp = _OPENAI_CLIENT.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
            n=1,
        )
        b64_data = resp.data[0].b64_json
        return b64_data, "🧙 Item art generated via gpt-image-1."
    except Exception as e:
        return None, f"⚠️ Image generation failed: {e}"


def save_image_to_file(b64_png, item_name):
    """
    Save the base64 PNG data to disk alongside this script in an 'images' folder.
    Returns the file path or None on failure.
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(base_dir, "images")
        os.makedirs(img_dir, exist_ok=True)

        # Simple slug from item name
        slug = "".join(
            c.lower() if c.isalnum() else "_" for c in (item_name or "item")
        )[:40]
        filename = f"{slug}.png"
        path = os.path.join(img_dir, filename)

        with open(path, "wb") as f:
            f.write(base64.b64decode(b64_png))
        return path
    except Exception:
        return None


def resize_image_to_height(img_path, target_height=350):
    """Resize image to a target pixel height, preserving aspect ratio.

    Prefers Pillow; falls back to ImageMagick `convert` if Pillow is missing.
    Returns the path to the resized image (or the original path on failure).
    """
    # Try Pillow first
    if Image is not None:
        try:
            im = Image.open(img_path)
            width, height = im.size
            if height <= target_height:
                return img_path
            scale = target_height / float(height)
            new_width = max(1, int(width * scale))
            im = im.resize((new_width, target_height), Image.LANCZOS)
            base, ext = os.path.splitext(img_path)
            new_path = f"{base}_h{target_height}{ext}"
            im.save(new_path, format="PNG")
            return new_path if os.path.exists(new_path) else img_path
        except Exception:
            pass

    # Fallback: ImageMagick convert, if available
    if shutil.which("convert") is not None:
        try:
            base, ext = os.path.splitext(img_path)
            new_path = f"{base}_h{target_height}{ext}"
            subprocess.run(
                ["convert", img_path, "-resize", f"x{target_height}", new_path],
                check=False,
            )
            if os.path.exists(new_path):
                return new_path
        except Exception:
            pass

    # If everything fails, just return the original
    return img_path


def show_image_if_supported(img_path):
    """
    Display the image after the text card using sixel/img2sixel.

    This requires `img2sixel` to be installed and a sixel-capable terminal.
    Set DNDGEN_NO_INLINE=1 to disable this behavior.

    Returns True if we attempted inline display, False otherwise.
    """
    no_inline = os.getenv("DNDGEN_NO_INLINE", "").lower()
    if no_inline in ("1", "true", "yes"):
        return False

    if shutil.which("img2sixel") is None:
        return False

    # Determine target pixel height (default 350px, overridable via env var)
    try:
        target_h = int(os.getenv("DNDGEN_IMG_HEIGHT", "350"))
    except ValueError:
        target_h = 350

    img_for_display = resize_image_to_height(img_path, target_height=target_h)

    # Emit sixel image via img2sixel at the resized pixel dimensions
    try:
        subprocess.run(["img2sixel", img_for_display], check=False)
    except Exception:
        return False

    return True


# ==========================
#   FRAMING & RENDERING
# ==========================

def framed_block(lines, border_color=BRIGHT_BLUE):
    """
    Previously drew a box border; now just returns the content lines.
    Border was dropped to avoid occasional alignment issues with wide glyphs.
    """
    return list(lines)


def render_item_card(item, enhancement_note=""):
    rarity_str = f"{item['rarity_emoji']} {item['rarity_name']}"
    rarity_str_colored = color(rarity_str, item["rarity_color"], BOLD)
    name_str = color(item["name"], BRIGHT_YELLOW, BOLD)

    type_line = (
        color("Type: ", BRIGHT_CYAN, BOLD)
        + f"{item['quality']} {item['material']} {item['type']}"
    )
    rarity_line = color("Rarity: ", BRIGHT_CYAN, BOLD) + rarity_str_colored

    mech_line = color("Mechanic: ", BRIGHT_CYAN, BOLD) + item["effect"]
    attune_line = color("Attunement: ", BRIGHT_CYAN, BOLD) + item["attune"]

    enh_lore = item.get("enhanced_lore")
    enh_quirk = item.get("enhanced_quirk")

    wrapper = textwrap.TextWrapper(width=70)

    if enh_lore:
        lore_text = enh_lore
    else:
        lore_text = (
            f"Forged origin: {item['origin']}. "
            f"Its magic is such that {item['enchantment']}."
        )

    if enh_quirk:
        quirk_text = enh_quirk
    else:
        quirk_text = f"Quirk: {item['quirk']}."

    lore_lines = wrapper.wrap(lore_text)
    quirk_lines = wrapper.wrap(quirk_text)

    mech_note = item.get("mechanical_note")
    mech_note_lines = wrapper.wrap(mech_note) if mech_note else []

    body = [
        name_str,
        rarity_line,
        type_line,
        "",
        mech_line,
        attune_line,
        "",
    ]

    body.append(color("📝 Lore:", BRIGHT_MAGENTA, BOLD))
    body.extend(lore_lines)
    body.append("")
    body.append(color("✨ Oddities:", BRIGHT_MAGENTA, BOLD))
    body.extend(quirk_lines)

    if mech_note_lines:
        body.append("")
        body.append(color("⚖️ GM Note:", BRIGHT_MAGENTA, BOLD))
        body.extend(mech_note_lines)

    if enhancement_note:
        body.append("")
        body.append(color(enhancement_note, BRIGHT_BLACK, DIM))

    return framed_block(body, border_color=BRIGHT_BLUE)


def slow_print(lines, delay=0.01):
    """Print lines with a subtle scrolling effect."""
    for line in lines:
        print(line)
        time.sleep(delay)


# ==========================
#   MAIN LOOP
# ==========================

def main():
    clear_screen()
    print_banner()

    while True:
        user_input = input(
            color("✨ [Enter] forge AI-boosted item  |  'q' quit > ", BRIGHT_GREEN, BOLD)
        )
        if user_input.strip().lower().startswith("q"):
            print(color("May your loot be ever shiny. Farewell! 🧵✨", BRIGHT_CYAN))
            break

        clear_screen()
        print_banner()

        base_item = generate_base_item()
        enhanced_item, note = enhance_with_openai(base_item)

        # Generate an image (if possible) and save to disk
        image_b64, image_status = generate_item_image(enhanced_item)
        img_path = None
        image_note = image_status
        if image_b64:
            img_path = save_image_to_file(image_b64, enhanced_item.get("name"))
            if img_path:
                image_note = f"{image_status} Saved to {img_path}."

        combined_note_parts = [note, image_note]
        combined_note = " ".join(p for p in combined_note_parts if p).strip()

        card = render_item_card(enhanced_item, enhancement_note=combined_note)
        slow_print(card, delay=0.004)

        # Render the image after the text card using sixel/img2sixel (if available)
        if img_path:
            print()  # spacer line before image
            show_image_if_supported(img_path)
        print()
        print(
            color("💡 Tip:", BRIGHT_BLACK, BOLD),
            color("Use this as inspiration; adjust numbers to fit your table.", BRIGHT_BLACK),
        )
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(color("Interrupted by user. May your dice roll high! 🎲", BRIGHT_CYAN))
