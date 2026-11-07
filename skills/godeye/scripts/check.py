import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def ids_in(pattern, text):
    return set(re.findall(pattern, text))


def quoted_ids(block):
    return set(re.findall(r'"([a-z0-9-]+)"', block))


def main(path):
    html = Path(path).read_text(encoding="utf-8")
    problems = []

    match = re.search(r"<script>(.*?)</script>", html, re.S)
    if not match:
        print("no inline script found")
        return 1
    script = match.group(1)

    nodes = ids_in(r'data-id="([a-z0-9-]+)"', html)
    details = set(re.findall(r'^\s*"([a-z0-9-]+)": \{', script, re.M))
    ends = ids_in(r'data-[ab]="([a-z0-9-]+)"', html)
    extras = {word for group in re.findall(r'data-x="([^"]+)"', html) for word in group.split()}
    links = {name for group in re.findall(r"links: \[([^\]]*)\]", script) for name in quoted_ids(group)}

    kids_block = re.search(r"var KIDS = (\{.*?\});", script, re.S)
    kids = quoted_ids(kids_block.group(1)) if kids_block else set()
    frame_block = re.search(r"var FRAME = (\{.*?\});", script, re.S)
    frame_rects = quoted_ids(frame_block.group(1)) if frame_block else set()
    rect_ids = ids_in(r'<rect id="([a-z0-9-]+)"', html)

    checks = [
        ("boxes without details", nodes - details),
        ("details without a box", details - nodes),
        ("edge ends that are not boxes", (ends | extras) - nodes),
        ("links that are not boxes", links - details),
        ("children that are not boxes", kids - nodes),
        ("frame rects that do not exist", frame_rects - rect_ids),
    ]
    for label, missing in checks:
        if missing:
            problems.append(f"{label}: {', '.join(sorted(missing))}")

    dashes = html.count("—") + html.count("–")
    if dashes:
        problems.append(f"em or en dashes: {dashes}")

    node_bin = shutil.which("node")
    if node_bin:
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as handle:
            handle.write(script)
            script_path = handle.name
        result = subprocess.run([node_bin, "--check", script_path], capture_output=True, text=True)
        Path(script_path).unlink(missing_ok=True)
        if result.returncode != 0:
            problems.append("script does not parse: " + (result.stderr.strip().splitlines() or ["unknown error"])[-1])
    else:
        problems.append("node not found, script syntax not checked")

    if problems:
        for problem in problems:
            print(problem)
        return 1
    edge_count = len(re.findall(r'class="ed', html))
    print(f"ok: {len(nodes)} boxes, {edge_count} edges")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 -I check.py <page.html>")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
