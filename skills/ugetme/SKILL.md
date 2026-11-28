---
name: ugetme
description: Show the user what you understood from their prompts, what you would add or change in their ask if anything, and a short plan of what you will do, then ask for their go with AskUserQuestion, showing that plan in the dialog itself, and do no work until they give it. Run it before every big task, meaning one where a misread costs real rework, and whenever the user types /ugetme. Skip it for small obvious tasks.
argument-hint: <the task>
---

# ugetme

The user wants proof that you understood them, and your honest view of their ask, before any real work starts.

Task:

$ARGUMENTS

If the task above is empty, use the user's prompts for the current task instead: every message since the task started, with each later correction replacing what it corrects.

## What to reply

Write the reply from the prompts, the rules, memory and earlier messages, plus a quick look at what already exists on the topic when that could change the answer. Do none of the task's real work first.

The reply has exactly three parts of chat text, each under its bold label, followed by the ask described below, and nothing else: no intro line, no closing line.

**What I understood**

- The first bullet says what the user is really after: the outcome they want and the problem it removes for them.
- Then one bullet for each thing the user will get when you are done.
- One bullet for what stays out, only when the scope could be misread.
- Where the prompt reads two ways, write the reading you picked as a plain bullet here.

**What I would add or change**

- One bullet for each thing you would add or change: something the ask needs but leaves out, a place where it is wrong or clashes with something already decided or already built, or a simpler or better route.
- For an addition, say what you would add and why. For a change, say what the user asked, what you would do instead, and why. Keep each to one or two sentences, so a plain "go" accepts it.
- When there is nothing to add or change, this part is one line: "Nothing, it holds as you said it."

**The plan**

- 3 to 6 numbered steps of what you will do, in the order you will do them, one short line each.
- Each step names the real file, page or feature it touches, so the user sees where the work lands.
- Steps that come from What I would add or change are part of the plan, so a plain "go" builds exactly this plan.

Rules for all three parts:

- Talk to the user as "you", in simple English and in your own words. Repeating or reshuffling their phrasing proves nothing. Keep only the real names of the files, pages and features they mentioned.
- Under What I understood and What I would add or change, say what the user will end up with, not how you will build it. The how goes only under The plan. No lists of options anywhere.
- No questions in the bullets: the ask is the only question.
- Never correct the user's English.
- Usually 3 to 6 bullets under What I understood. More means they are too detailed.

Example, for a request to save Inbox filters and give the whole team one default filter:

Echo, wrong:

- In the Inbox, save filters like open convs + unread, switch between them, use none of them, or make one the default for the team.

Understood, right:

**What I understood**

- You want to stop rebuilding the same Inbox filters by hand: the sets you use often stay one click away, and the Inbox opens on the one you work from.
- You get filter sets you can save under a name, switch between, and clear back to no filter.
- You get one set marked as the default the Inbox opens on.

**What I would add or change**

- You asked for one default for the whole team. I would let each person pick their own default and keep the saved sets shared, because two agents rarely work from the same filter.
- I would also let you rename a saved set, because names go stale as your work changes.

**The plan**

1. Add saved filter sets to the Inbox, shared by the whole team, with rename.
2. Let each person mark one set as the default their Inbox opens on.
3. Add the set picker to the Inbox page, with its empty and failed states.

Then the ask, with the question "Did I get you right? You want to stop rebuilding the same Inbox filters by hand." and the options Go (Recommended), Go as I asked and Not yet. The preview on Go (Recommended):

```
What you get
- Saved filter sets, shared, renamable
- Your own default set

The plan
1. Saved sets in the Inbox, shared
   by the team, with rename
2. A default set per person
3. The set picker in the Inbox page
```

The reply is allowed even though it comes before the work: it is an exception to any rule about keeping replies terse, which still governs everything after it.

## The ask

Right after the three parts, call AskUserQuestion once, with one single-select question, so the user gets a notification. The dialog can hide the chat text, so it carries the plan itself, in the previews. If AskUserQuestion is not available, end the reply after the three parts and wait for the go in the chat.

- Header: `ugetme`.
- Question: "Did I get you right?" followed by the first bullet of What I understood, reworded as one sentence. Plain text on one line, under 200 characters in all: the dialog runs line breaks together and the notification cuts the text at 200 characters.
- Options, in this order:
  - `Go (Recommended)`, described as "Build it as written above, with what I would add or change." When there is nothing to add or change, the description is "Build it as written above."
  - `Go as I asked`, described as "Build only your ask, without what I would add or change." Leave it out when there is nothing to add or change.
  - `Not yet`, described as "Do nothing yet. Answer in the chat when you are ready."
- Previews, so the dialog shows what will be built without the chat:
  - `Go (Recommended)`: "What you get", with the bullets of What I understood after the first one, then "The plan", with its numbered steps.
  - `Go as I asked`: the same, without anything from What I would add or change.
  - `Not yet`: no preview.
  - The preview box does not wrap, so keep every line under 40 characters and move the rest of a long item to an indented next line. Plain text only: no bold, links or code.

## Then stop

After the ask, do no work, no other tool calls and no investigation until the user gives the go.

- `Go (Recommended)`, or "go", "ok", "yes", "do it" or similar typed in Other or in the chat, with or without corrections: the go also accepts every point under What I would add or change that the user did not push back on. Apply the corrections and do the task, without repeating the bullets. Notes added to a picked option count as corrections.
- `Go as I asked`: drop every point under What I would add or change, apply any corrections, and do the task as the user asked it.
- Corrections without a go, typed in Other or in the chat: show only the bullets and steps that changed, under the same three labels, then ask again the same way.
- `Not yet`, a dismissed question, or a result saying nobody answered or the question timed out: that is no go. End the turn with one line saying you are waiting for their go, and do nothing else. Never fall back on your own judgment to start the work.
