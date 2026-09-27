# sqlite-memory

A Claude Code skill for token-lean persistent project memory. Facts live in a SQLite FTS5 table (`.claude/memory.db`) and are retrieved by keyword search, so only the few relevant rows enter context instead of a large CLAUDE.md or notes folder.

## Install

```
git clone https://github.com/ghulqdev/sqlite-memory ~/.claude/skills/sqlite-memory
```

Requires Python 3 with SQLite FTS5 (included in standard CPython builds). No other dependencies.

## Usage

```
python ~/.claude/skills/sqlite-memory/mem.py search "auth session" -n 5
python ~/.claude/skills/sqlite-memory/mem.py add decision db "Postgres over Mongo: relational joins on accounts." -i 5
python ~/.claude/skills/sqlite-memory/mem.py update 2 "new text"
python ~/.claude/skills/sqlite-memory/mem.py delete 2
python ~/.claude/skills/sqlite-memory/mem.py topics
```

See `SKILL.md` for the memory protocol Claude follows.

## License

MIT
