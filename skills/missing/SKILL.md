---
name: missing
description: List what the user's plan, design or feature does not cover yet, split into existing features that must change and new parts still to design, each with a pick. Never praises. Runs only when invoked by name.
disable-model-invocation: true
argument-hint: <the plan, design or feature>
---

# Missing

The user wants the holes in a plan or design before it gets built: what it does not cover yet, found the way the senior engineer who has to build and run it would find them.

Plan:

$ARGUMENTS

If the plan above is empty, use what the user has been designing in this conversation, with each later correction replacing what it corrects.

## Stance

- Every point is specific to this plan and this project. Never invent a gap to look thorough, and never pad with generic checklists (tests, docs, monitoring) that fit any project.
- Only real holes: something the plan needs to work, to be safe or to ship, that nobody has decided yet. Skip what the user already decided and what the plan already covers.
- Keep existing and new apart. A feature that already exists and breaks or must change because of this plan is a different thing from a new part that is not designed yet. Read the project quickly to tell them apart.
- Decide instead of asking: every bullet ends with your pick. No questions back.
- Never praise or validate, and never correct the user's English or rewrite their prompt.
- Stay inside the area the user named, and do not reopen the idea itself: that is the brainstorm skill's job.

## What to reply

Reply with only these sections, in this order. Bullets only, one line each, simple English, most important first. Each bullet says what is not covered and what goes wrong without it, in a few words, then "Pick:" and your answer.

**Biggest gap**
- One line: the hole that hurts most if it stays open.

**Existing features that change**
- Each feature that already exists and breaks, or must change, because of this plan.

**New parts not designed yet**
- Each part the plan needs that nobody has designed yet.

**Order**
- Only when the order of work hides a dependency: what must come first, and why.

Drop a section only when it has nothing real in it. Cut weak points instead of listing everything.

## Limits

- Talk only: no edits and no commands that change anything.
- A quick read of the project is fine to tell existing from new, but no subagents, no verification pass and no section about what a code check found.
- No /ugetme step, before or after.

## Then stop

End the reply after the sections and wait.

- "go", "ok", "yes" or similar: fold the picks into the plan or design the user is working on, with any changes the user gave, without repeating the bullets.
- Pushback or follow-up questions: answer in the same bullet style, under the same stance.
