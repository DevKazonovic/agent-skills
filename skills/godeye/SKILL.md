---
name: godeye
description: Build a god view of a system, one map that draws every app, service, container, store and outside dependency on a single canvas with the calls between them, where clicking any part opens a slideover with its details and lights up everything it connects to. The skill writes the map as one godeye file in a fixed JSON format, and the Godeye page of the MyTools app draws it. Use it when the user types /godeye, or asks for an architecture diagram, a system map, a visual of the whole system, or how a feature works end to end across repos, even when they do not name the format. Not for a single flow chart, a data model on its own, UI wireframes or a slide deck.
argument-hint: <the system, feature or repos to map>
---

# godeye

One canvas, the whole system, details on click. The user wants to see everything at once and drill into the part they care about. You write the map as data in one `*.godeye.json` file, and the Godeye page in MyTools draws it: it places the boxes, routes the lines, opens the slideovers and lights up connections. You never write HTML, SVG, coordinates or styles. The page draws any file it is given, and when something in the file is wrong it still draws the rest and lists each problem, so a bad file shows up as a list of problems, not a blank page.

## Steps

1. **Get every repo on disk first.** Map from code, never from memory or from one side of a call. List the services the code talks to: HTTP clients, env keys ending in `_URL`, queue names, compose services, webhooks, internal callback routes. When a service's code is missing, find its repo (the workspace setup script, the org's repo names, the git remotes of the repos already there), clone it next to the others the same way they were cloned, and say so in one line. If the workspace has a setup script that clones repos, add the new one there too so the next developer gets it. A box drawn only from the caller's side hides exactly the logic the user wants to see; this skill exists because an AI engine was first drawn as a black box and its context handling went missing.
2. **Read the system, evidence first.** For each service, find its entry points (routes, GraphQL schema, listeners, controllers, commands), its main runtime loop, queues and schedules (cron, Celery beat, Horizon), stores (schema files, migrations, `prod.sql`, models), outside calls (model providers, payments, crawlers, email), security boundaries (secrets by env key name only, auth on internal routes), deploy topology (compose files, containers, CPU and memory, networks) and limits (timeouts, retries, batch sizes, TTLs, concurrency). Keep the file path for every fact. Mark anything you could not read as inferred. Read in one thread; use subagents or workflows only when the user asks for them by name.
3. **Plan the grid** (Layout below): which band each part sits in, and its column.
4. **Write the file** in the format below, by hand with the Write tool. Save it in the project that owns the system, in the backend's `docs/reports/<topic>/<topic>.godeye.json`. The Godeye page lists every file whose name ends in `.godeye.json`. Start from `assets/example.json` when it helps.
5. **Check once:** `python3 -I <skill-dir>/scripts/check.py <file>`. It runs the same checks as the Godeye page and also flags missing details and em or en dashes. Fix what it reports and run it once more.
6. **Reply in a few lines:** the link `http://localhost:3783/godeye/<path>`, where `<path>` is the file's path under `~/Projects` without `.godeye.json`, then what the canvas covers, which box holds the part the user asked about, and anything that could not be mapped. To update a map, write the same file again; the link stays the same.

## Format

One JSON object. Ids are kebab-case and unique across the whole file. Unknown fields are ignored.

```json
{
  "godeye": 1,
  "title": "AI Agents V2",
  "system": "eGrow",
  "summary": "How a customer message becomes an AI reply.",
  "live": "a customer message to its reply",
  "bands": [ { "title": "People and apps", "items": [ ... ] } ],
  "edges": [ { "from": "customer", "to": "channels", "label": "chats", "live": true, "both": true } ]
}
```

- `godeye`: always `1`. `title` is required. `system`, `summary` (one line, shown in the map list) and `live` (what the accent path is) are optional.
- `columns`: optional. The grid is as wide as the widest column used; 7 columns fit best.
- `bands`: the canvas from top to bottom. A band has an optional `title` (a small heading such as "Stores and outside"), an optional `"layout": "spread"`, and `items`.
- An item is a box, a zone or a frame:
  - **box**: `{ "id", "title", "note", "col", "span" }`. `title` up to about 18 characters. `note` is one short line, or a list of short lines for a core module. `col` is required (1 is the left column); `span` is how many columns it covers (default 1). A note that is a route or a path shows in mono. Text that does not fit wraps.
  - **zone**: `{ "id", "type": "zone", "title", "col", "span", "items" }`: a stack such as a backend or an engine, drawn as a shaded area. Without `col` and `span` it covers the whole width of its band.
  - **frame**: `{ "id", "type": "frame", "title", "col", "span", "items" }`: a container or a group inside a zone, drawn with a dashed border. Its boxes are drawn a little smaller.
  - The items of a zone or frame use the same columns as the whole canvas and must sit inside the columns of their parent.
  - Items that share a column stack from top to bottom in the order you list them. A box spanning columns starts below the lowest item in any of those columns.
  - `"layout": "spread"` on a band, zone or frame ignores `col` and shares the full width between its boxes in one row. Use it for the database bar of table groups.
- Every box, zone and frame takes its details in the same object: `kind` (where it runs, such as "Backend · queue"), `lead` (one sentence), `blocks` and `code` (file paths). A block is `{ "title": "Limits", "list": [...] }`, `{ "steps": [...] }` (a flow in its real order) or `{ "kv": [["Timeout", "10 s"], ...] }`. `title` is optional. Text in backticks shows as code.
- `edges`: `from` and `to` are ids of boxes, zones or frames. `label` is one or two words or a route. `live: true` puts the edge on the accent path. `both: true` draws arrows at both ends. `lights` lists more ids whose selection lights this edge up. Connect a zone to the database zone with one edge and `lights` instead of an edge from every box.
- The panel's "Connected to" buttons come from the edges and from each part's parent and children, so you never list them.

## Layout

- Bands from top to bottom: people and the apps they use; each backend stack as a zone; each engine or worker stack as a zone, with its containers as frames and their modules inside; stores and outside services; the main database as a spread zone of table groups at the bottom.
- Put each box in the column of the box that calls it, so most lines are straight. Give a module that many others call the middle column.
- Two zones can share a band side by side when each one sets `col` and `span`.

## Details

- Two to five short blocks per part, then Code. Use real names and numbers from the code: routes, queue names, timeouts, retries, batch sizes, TTLs, model names, table names, file paths.
- Put security notes and gaps in the part they belong to, stated plainly.
- Write in plain words and short sentences, with no em or en dashes. Never put secret values, tokens or production hostnames in the file; env key names and internal service names are fine.

## Files

- `assets/example.json`: a small complete map that uses every field.
- `scripts/check.py`: the check from step 5.
