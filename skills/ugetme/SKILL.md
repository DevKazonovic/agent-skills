---
name: ugetme
description: Show the user what you understood from their prompts, then what should change in their ask if anything, and stop and wait for their go before doing any work. Run it before every big task, meaning one where a misread costs real rework, and whenever the user types /ugetme. Skip it for small obvious tasks.
argument-hint: <the task>
---

# ugetme

The user wants proof that you understood them, and your honest view of their ask, before any real work starts.

Task:

$ARGUMENTS

If the task above is empty, use the user's prompts for the current task instead: every message since the task started, with each later correction replacing what it corrects.

## What to reply

Write the reply from the prompts, the rules, memory and earlier messages, plus a quick look at what already exists on the topic when that could change the answer. Do none of the task's real work first.

The reply has exactly two parts, each under its bold label, and nothing else: no intro line, no closing line.

**What I understood**

- The first bullet says what the user is really after: the outcome they want and the problem it removes for them.
- Then one bullet for each thing the user will get when you are done.
- One bullet for what stays out, only when the scope could be misread.
- Where the prompt reads two ways, write the reading you picked as a plain bullet here.

**What it should be instead**

- One bullet for each place where the ask is wrong, clashes with something already decided or already built, or has a simpler or better route. Say what the user asked, what you would do instead, and why, in one or two sentences, so a plain "go" accepts it.
- When nothing needs to change, this part is one line: "Nothing, it holds as you said it."

Rules for both parts:

- Talk to the user as "you", in simple English and in your own words. Repeating or reshuffling their phrasing proves nothing. Keep only the real names of the files, pages and features they mentioned.
- Say what the user will end up with, not how you will build it: no steps and no lists of options.
- No questions.
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

**What it should be instead**

- You asked for one default for the whole team. I would let each person pick their own default and keep the saved sets shared, because two agents rarely work from the same filter.

The reply is allowed even though it comes before the work: it is an exception to any rule about keeping replies terse, which still governs everything after it.

## Then stop

End the reply after the two parts. Do no work, no tool calls and no investigation until the user answers.

- "go", "ok", "yes", "do it" or similar, with or without corrections: the go also accepts every point under What it should be instead that the user did not push back on. Apply the corrections and do the task, without repeating the bullets.
- Corrections without a go: show only the bullets that changed, under the same two labels, then wait again.
