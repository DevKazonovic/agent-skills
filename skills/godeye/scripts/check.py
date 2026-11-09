import json
import re
import sys
from pathlib import Path

VERSION = 1
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
TYPES = {"box", "zone", "frame"}
MAX_COLUMNS = 12


def text(value):
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (str, int, float)):
        return str(value).strip()
    return ""


def whole(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().lstrip("-").isdigit():
        return int(value.strip())
    return None


def widest(value, found=1):
    if isinstance(value, list):
        for item in value:
            found = max(found, widest(item, found))
        return found
    if not isinstance(value, dict):
        return found
    col = whole(value.get("col"))
    span = whole(value.get("span")) or 1
    reach = col + max(1, span) - 1 if col is not None and col >= 1 else found
    return max(found, reach, widest(value.get("items"), found), widest(value.get("bands"), found))


class Checker:
    def __init__(self):
        self.problems = []
        self.ids = set()
        self.counts = {"box": 0, "zone": 0, "frame": 0}

    def problem(self, message):
        self.problems.append(message)

    def details(self, raw, part_id):
        blocks = raw.get("blocks")
        good_blocks = 0
        if blocks is not None and not isinstance(blocks, list):
            self.problem(f'The blocks of "{part_id}" are not a list.')
        for index, block in enumerate(blocks if isinstance(blocks, list) else [], start=1):
            if not isinstance(block, dict):
                self.problem(f'Block {index} of "{part_id}" is not an object.')
            elif not any(isinstance(block.get(key), list) for key in ("list", "steps")) and not isinstance(block.get("kv"), (list, dict)):
                self.problem(f'Block {index} of "{part_id}" has no "list", "steps" or "kv".')
            else:
                good_blocks += 1
        if not text(raw.get("lead")) and not good_blocks:
            self.problem(f'"{part_id}" has no details: add a "lead" and blocks.')

    def item(self, raw, parent, position):
        if not isinstance(raw, dict):
            self.problem(f"Item {position} in {parent['label']} is not an object.")
            return
        part_id = text(raw.get("id"))
        title = text(raw.get("title"))
        if not part_id:
            name = f'"{title}"' if title else f"Item {position}"
            self.problem(f"{name} in {parent['label']} has no id.")
            part_id = f"item {position} in {parent['label']}"
        elif part_id in self.ids:
            self.problem(f'Two parts use the id "{part_id}". The second one is not drawn.')
            return
        elif not ID_PATTERN.match(part_id):
            self.problem(f'The id "{part_id}" should use only lowercase letters, numbers and dashes.')
        self.ids.add(part_id)
        kind = raw.get("type")
        if kind in TYPES:
            item_type = kind
        else:
            item_type = ("zone" if parent["type"] == "band" else "frame") if isinstance(raw.get("items"), list) else "box"
            if kind is not None:
                self.problem(f'"{part_id}" has the type "{text(kind)}", which is not box, zone or frame.')
        self.counts[item_type] += 1
        if not title:
            self.problem(f'"{part_id}" has no title.')
        self.details(raw, part_id)
        col_range = parent["range"]
        if parent["layout"] != "spread":
            col = whole(raw.get("col"))
            span = whole(raw.get("span"))
            if item_type != "box" and col is None and span is None:
                col, span = col_range[0], col_range[1] - col_range[0] + 1
            else:
                if span is None or span < 1:
                    if raw.get("span") is not None:
                        self.problem(f'"{part_id}" has a span that is not a whole number of 1 or more.')
                    span = 1
                if col is None:
                    self.problem(f'"{part_id}" has no column.')
                    col = col_range[0]
                if col < col_range[0] or col + span - 1 > col_range[1]:
                    self.problem(f'"{part_id}" covers columns {col} to {col + span - 1}, outside {parent["label"]} (columns {col_range[0]} to {col_range[1]}).')
                    span = min(span, col_range[1] - col_range[0] + 1)
                    col = min(max(col, col_range[0]), col_range[1] - span + 1)
            inner = (col, col + span - 1)
        else:
            inner = col_range
        if item_type == "box":
            if raw.get("items") is not None:
                self.problem(f'"{part_id}" is a box, so its items are not drawn. Make it a zone or a frame.')
            return
        layout = raw.get("layout")
        if layout is not None and layout != "spread":
            self.problem(f'"{part_id}" has the layout "{text(layout)}". The only layout is "spread".')
            layout = None
        self.items(raw.get("items"), {"type": item_type, "label": f'"{part_id}"', "range": inner, "layout": layout or parent["layout"]})

    def items(self, value, parent):
        if value is None:
            if parent["type"] != "band":
                self.problem(f"{parent['label']} has no \"items\".")
            return
        if not isinstance(value, list):
            self.problem(f"The items of {parent['label']} are not a list.")
            return
        for position, raw in enumerate(value, start=1):
            self.item(raw, parent, position)

    def bands(self, value, columns):
        if not isinstance(value, list) or not value:
            self.problem('"bands" must be a list with at least one band.')
            return
        for index, raw in enumerate(value, start=1):
            if not isinstance(raw, dict):
                self.problem(f"Band {index} is not an object.")
                continue
            title = text(raw.get("title"))
            label = f'the band "{title}"' if title else f"band {index}"
            layout = raw.get("layout")
            if layout is not None and layout != "spread":
                self.problem(f'{label} has the layout "{text(layout)}". The only layout is "spread".')
                layout = None
            if not isinstance(raw.get("items"), list) or not raw.get("items"):
                self.problem(f"{label} has no items.")
            self.items(raw.get("items"), {"type": "band", "label": label, "range": (1, columns), "layout": layout})

    def edges(self, value):
        if value is None:
            return 0
        if not isinstance(value, list):
            self.problem('"edges" is not a list.')
            return 0
        drawn = 0
        for index, raw in enumerate(value, start=1):
            if not isinstance(raw, dict):
                self.problem(f"Edge {index} is not an object.")
                continue
            start, end = text(raw.get("from")), text(raw.get("to"))
            if not start or not end:
                self.problem(f'Edge {index} needs both "from" and "to".')
                continue
            missing = [name for name in dict.fromkeys([start, end]) if name not in self.ids]
            if missing:
                names = " and ".join(f'"{name}"' for name in missing)
                self.problem(f'The edge from "{start}" to "{end}" points at {names}, which does not exist.')
                continue
            if start == end:
                self.problem(f'The edge from "{start}" to itself is not drawn.')
                continue
            for light in raw.get("lights") or []:
                if text(light) not in self.ids:
                    self.problem(f'The edge from "{start}" to "{end}" lights up "{text(light)}", which does not exist.')
            drawn += 1
        return drawn


def main(path):
    source = Path(path).read_text(encoding="utf-8")
    try:
        raw = json.loads(source)
    except json.JSONDecodeError as error:
        print(f"not valid JSON at line {error.lineno}, column {error.colno}: {error.msg}")
        return 1
    if not isinstance(raw, dict):
        print("the file must hold one JSON object")
        return 1
    checker = Checker()
    if raw.get("godeye") != VERSION:
        checker.problem(f'"godeye" must be {VERSION}.')
    if not text(raw.get("title")):
        checker.problem('The map has no "title".')
    declared = whole(raw.get("columns"))
    if raw.get("columns") is not None and (declared is None or declared < 1):
        checker.problem('"columns" is not a whole number of 1 or more.')
    columns = max(declared if declared and declared >= 1 else 1, widest(raw.get("bands")))
    if columns > MAX_COLUMNS:
        checker.problem(f"The map needs {columns} columns. Only {MAX_COLUMNS} fit.")
        columns = MAX_COLUMNS
    checker.bands(raw.get("bands"), columns)
    drawn = checker.edges(raw.get("edges"))
    dashes = source.count(chr(0x2014)) + source.count(chr(0x2013))
    if dashes:
        checker.problem(f"em or en dashes: {dashes}")
    if checker.problems:
        for problem in checker.problems:
            print(problem)
        return 1
    containers = checker.counts["zone"] + checker.counts["frame"]
    print(f"ok: {checker.counts['box']} boxes, {containers} zones and frames, {drawn} edges")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 -I check.py <map.godeye.json>")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
