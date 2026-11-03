"""Regenerate games.json from the tables in README.md.

Usage: python3 scripts/build_data.py
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {"Contents", "Start here: the big ones"}
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def main():
    games, seen, section = [], set(), None
    for line in (ROOT / "README.md").read_text().splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if section is None or section in SKIP:
            continue
        if line.startswith("| ") and not line.startswith(("| Game", "| Site", "|---")):
            cells = [c.strip() for c in line.strip("|").split("|")]
            name_cell, desc = cells[0], cells[1]
        elif line.startswith("- ["):
            name_cell, _, desc = line[2:].partition(": ")
        else:
            continue
        featured = "⭐" in name_cell
        for name, url in LINK.findall(name_cell):
            if url in seen:
                continue
            seen.add(url)
            games.append({
                "name": name.strip(),
                "url": url,
                "description": LINK.sub(r"\1", desc).replace("**", "").strip(),
                "category": section,
                "featured": featured,
            })
    (ROOT / "games.json").write_text(json.dumps(games, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {len(games)} games")


if __name__ == "__main__":
    main()
