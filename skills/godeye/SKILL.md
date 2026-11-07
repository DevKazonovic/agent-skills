---
name: godeye
description: Build a god view of a system, one interactive page that draws every app, service, container, store and outside dependency on a single canvas with the calls between them, where clicking any part opens a slideover with its details and lights up everything it connects to. Use it when the user types /godeye, or asks for an architecture diagram, a system map, a visual of the whole system, or how a feature works end to end across repos, even when they do not name the format. Not for a single flow chart, a data model on its own, UI wireframes or a slide deck.
argument-hint: <the system, feature or repos to map>
---

# godeye

One canvas, the whole system, details on click. The user wants to see everything at once and drill into the part they care about, so the page is the diagram and nothing else: no intro section, no tables, no extra pages around it. Depth lives in the slideover, never in more sections.

## What the page is

- A thin top bar (name, legend, zoom) and one SVG canvas filling the rest of the screen.
- Bands from top to bottom: people and the apps they use; each backend stack as a zone; each engine or worker stack as a zone, with its containers as dashed frames and their modules inside; stores and outside services; the main database as a bar across the bottom, split into table groups.
- Every box, frame title and zone title is clickable and keyboard focusable. A click opens a slideover on the right with that part's details; its edges and neighbours turn accent and everything else dims. Esc, the close button or a click on empty canvas closes it. Buttons in the slideover jump to the parts it connects to.
- One accent color, used for the main live path (for example a customer message to its reply) and for highlights. Everything else is neutral. Light and dark themes come from tokens.
- Zoom buttons: minus, Whole system (fits the whole canvas on screen), plus.

## Steps

1. **Get every repo on disk first.** Map from code, never from memory or from one side of a call. List the services the code talks to: HTTP clients, env keys ending in `_URL`, queue names, compose services, webhooks, internal callback routes. When a service's code is missing, find its repo (the workspace setup script, the org's repo names, the git remotes of the repos already there), clone it next to the others the same way they were cloned, and say so in one line. If the workspace has a setup script that clones repos, add the new one there too so the next developer gets it. A box drawn only from the caller's side hides exactly the logic the user wants to see; this skill exists because an AI engine was first drawn as a black box and its context handling went missing.
2. **Read the system, evidence first.** For each service, find its entry points (routes, GraphQL schema, listeners, controllers, commands), its main runtime loop, queues and schedules (cron, Celery beat, Horizon), stores (schema files, migrations, `prod.sql`, models), outside calls (model providers, payments, crawlers, email), security boundaries (secrets by env key name only, auth on internal routes), deploy topology (compose files, containers, CPU and memory, networks) and limits (timeouts, retries, batch sizes, TTLs, concurrency). Keep the file path for every fact. Mark anything you could not read as inferred. Read in one thread; use subagents or workflows only when the user asks for them by name.
3. **Build the inventory before drawing.** Nodes: kebab-case id, title (up to about 18 characters), one subtitle line (up to about 26 characters), band, column, kind, details. Edges: from, to, a one or two word label (a verb or the route), whether it is on the live path, and any extra ids that should light it up. Zones and frames: id, title, children.
4. **Lay it out on the grid** (Layout below).
5. **Write the details** (Details below).
6. **Build the page from `assets/template.html`.** Keep its CSS and script as they are. Replace the title, the bar text, the SVG body, the viewBox height if the canvas grows, and the `D`, `FRAME` and `KIDS` objects. Write the page by hand with the Write tool.
7. **Check once:** `python3 -I <skill-dir>/scripts/check.py <page.html>` confirms that the script parses, every box has details, every edge end, child and link points at a real box, and the page has no em or en dashes. Fix what it reports and run it once more.
8. **Save and publish.** Save the page in the project that owns the system, in the backend's `docs/reports/<topic>/<topic>.html`. When the user typed /godeye or asked for the page, publish it with the Artifact tool, which keeps it private. When the skill triggered from a question that did not ask for a page, save the file and offer the link in one line. To update a published map, publish the same file path again so the link stays the same.
9. **Reply in a few lines:** the link, what the canvas covers, which box holds the part the user asked about, and anything that could not be mapped.

## Layout

- The viewBox is 1600 wide. Use 7 columns of 180 px at x = 50, 270, 490, 710, 930, 1150 and 1370, with 40 px lanes between them; the column centres are 140, 360, 580, 800, 1020, 1240 and 1460.
- Boxes are 56 px tall; small modules 44 to 52 px; a core module with four short lines up to about 132 px.
- Band heights that fit a 1600 by 960 canvas: people and apps at y 34 to 90, the backend zone 126 to 340, the engine zone 376 to 744 with frames inside, stores and outside 780 to 836, the database bar 864 to 948. Keep the total height near 0.6 of the width so Whole system stays readable.
- Put each box under the box that calls it, so most edges are straight verticals. Route the rest as right-angle elbows through the 40 px lanes and the gaps between bands. Never route a line through a box.
- Allow at most one or two crossings; give the later edge a short halo, a 7 px stroke in the page background color over the crossing, so it reads as passing over.
- Label every edge with one or two words placed in the lane or gap beside the line; set route names in mono. Rotate a label only for a long connector in the margin.
- Join each stack to the database with one connector (the left margin for the first stack, a free column for the others) instead of an edge from every box.

## Details

Each part gets a kind (where it runs), a title, a one-sentence lead, then two to five short blocks, then Code and Connected to.

- Block types: `list` for facts, `steps` for a flow in its real order, `kv` for limits, settings and sizes.
- Use real names and numbers from the code: routes, queue names, timeouts, retries, batch sizes, TTLs, model names, table names, file paths.
- Put security notes and gaps in the part they belong to, stated plainly.
- Write in plain words and short sentences, with no em dashes. Never put secret values, tokens or production hostnames in the page; env key names and internal service names are fine.

## Look

- Zinc-like neutrals in light and dark. One accent: the product's brand color when its frontend theme defines one, else teal.
- Geist and Geist Mono from Google Fonts.
- Flat: borders only, no shadows. Container frames are dashed.

## Files

- `assets/template.html`: the working engine (bar, canvas, slideover, highlighting, keyboard, zoom) with a small example system to replace.
- `scripts/check.py`: the one-pass check from step 7.
