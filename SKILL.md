---
name: sqlite-memory
description: Token-lean persistent project memory stored in SQLite with FTS5 search. Use before architectural or design decisions to recall prior decisions, constraints, and bug root causes, and after substantial work to save reusable discoveries. Also use when the user says "remember this", "what did we decide about X", "check memory", or asks to save or forget a project fact. Never loads the whole store, only the top matches.
---

# SQLite Memory

Durable project knowledge lives in `.claude/memory.db` (relative to the project root, override with `MEMORY_DB`). One FTS5 table, queried selectively, so only 2 to 5 relevant rows ever enter context.

CLI (Python 3 stdlib only). `MEM` below means `python ~/.claude/skills/sqlite-memory/mem.py`, run from the project root.

```
MEM search "auth session token" [-n 5]
MEM add <category> <topic> "<content>" [-i 1..5]
MEM update <id> "<new content>"
MEM delete <id>
MEM topics
```

Categories: `decision`, `constraint`, `bug`, `gotcha`, `preference`, `reference`. Topic is one short kebab-case word or two (`auth`, `db-migrations`).

## Protocol

1. Never dump the database. No `select *`, no reading the .db file. Use `search` or `topics` only.
2. Before a decision touching architecture, conventions, or an area with history: run `search` with 2 to 5 specific keywords. If results look thin, try one synonym search. Stop there.
3. Treat results as background from the past. Verify a named file, function, or flag still exists before relying on it.
4. After substantial work, save only what is reusable and not derivable from code, git history, or docs:
   - why a choice was made, rejected alternatives
   - root causes of non-obvious bugs
   - external constraints, user preferences, gotchas
5. One fact per row, one or two sentences, include the why. Convert relative dates to absolute.
6. Before adding, `search` for an existing row on the same fact. `update` it instead of duplicating. `delete` rows that turned out wrong or obsolete.
7. Importance: 5 = must never be violated, 3 = default, 1 = nice to know. Higher importance ranks first on ties.
8. Keep CLAUDE.md small: permanent rules and a pointer to this skill. Everything situational goes here.

## Suggested CLAUDE.md snippet

```
## Memory
Project knowledge lives in `.claude/memory.db`, managed by the `sqlite-memory` skill.
Search it before architectural decisions. Never load it whole. Save reusable decisions after substantial work.
```

Add `.claude/memory.db` to version control if the team should share memory, or to `.gitignore` if it is personal.
