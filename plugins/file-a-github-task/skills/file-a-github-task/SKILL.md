---
name: File a GitHub task
description: >-
  Use this when creating or updating a GitHub issue/task so the write-up is
  complete before it is filed.
---
# File a GitHub task

Before creating the issue, collect a complete write-up. Fill anything the user already gave. Ask only for missing required fields. Do not stall on optional ones.

## Required

- **Title** — action-oriented, what to do
- **Why** — why this should be done
- **Acceptance criteria** — checkbox list of what done looks like
- **Assignee** — who builds it
- **QA** — who verifies (a person, @mentioned) **and** a checkbox checklist of things that should be tested. Ask if either the person or the test checklist is missing.

## Defaults (override if the user says otherwise)

- Type: Task
- Title prefix: ☑️ for tasks, 🛑 for bugs
- Optional metadata (priority, effort, start/target date): include if given, do not prompt unless the user mentioned them or they clearly matter

## Bugs also need

- Current vs expected behavior
- Repro steps, if the user has them
- Screenshots, if the user has them

## Issue body

```markdown
**Why**
<why it should be done>

**Acceptance criteria**
- [ ] <criterion>
- [ ] <criterion>

**QA**
@<qa-person>
- [ ] <what to test>
- [ ] <what to test>
```

For bugs, add **Current**, **Expected**, and **Repro** above the acceptance criteria.

## After filing

Reply with the issue link and a one-line recap of title, assignee, and QA.
