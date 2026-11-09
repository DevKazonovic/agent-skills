---
name: ugetme
description: Show the user, in short bullets, what you understood from their prompts, then stop and wait for their go before doing any work. Run it before every big task, meaning one where a misread costs real rework, and whenever the user types /ugetme. Skip it for small obvious tasks.
argument-hint: <the task>
---

# ugetme

The user wants proof that you understood them before any real work starts.

Task:

$ARGUMENTS

If the task above is empty, use the user's prompts for the current task instead: every message since the task started, with each later correction replacing what it corrects.

## What to reply

Write the bullets from the prompts alone, with no tool calls or investigation first, and reply with nothing else: no intro line, no closing line, no headings.

- **Goal:** your own reading of what the user is really after, in one line: the outcome they want and the problem it removes for them. Never their sentence handed back.
- One bullet for each thing the user will get when you are done.
- **Not doing:** what stays out, only when the scope could be misread.
- **Assuming:** each reading you picked where the prompt was unclear.

Rules for the bullets:

- One line each, in simple English and in your own words: say what you understood, never the user's phrasing repeated or reshuffled, because an echo proves nothing. Keep only the real names of the files, pages and features they mentioned.
- Say what the user will end up with, not how you will build it: no steps, no options, no reasons.
- No questions. Where the prompt can be read two ways, pick the reading that fits and list it under **Assuming**.
- Never correct the user's English.
- Usually 3 to 8 bullets. More means the bullets are too detailed.

Example, for a request to save Inbox filters and pick a default one:

- Echo, wrong: **Goal:** In the Inbox, save filters like open convs + unread, switch between them, use none of them, or make one the default.
- Understood, right: **Goal:** stop rebuilding the same Inbox filters by hand: the sets you use often stay one click away, and the Inbox opens on the one you work from.

The bullets are allowed even though they come before the work: they are an exception to any rule about keeping replies terse, which still governs everything after them.

## Then stop

End the reply after the bullets. Do no work, no tool calls and no investigation until the user answers.

- "go", "ok", "yes", "do it" or similar, with or without corrections: apply the corrections and do the task, without repeating the bullets.
- Corrections without a go: show only the bullets that changed, then wait again.
