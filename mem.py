import argparse
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "create virtual table if not exists memories using fts5(category, topic, content, importance unindexed, updated_at unindexed)"


def db_path() -> Path:
    return Path(os.environ.get("MEMORY_DB", ".claude/memory.db"))


def connect() -> sqlite3.Connection:
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute(SCHEMA)
    return conn


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def fts_query(text: str) -> str:
    return " OR ".join(f'"{w}"' for w in re.findall(r"\w+", text))


def show(rows) -> None:
    for rowid, category, topic, content, importance, updated in rows:
        print(f"#{rowid} [{category}/{topic}] (imp {importance}, {updated}) {content}")
    if not rows:
        print("no results")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(prog="mem")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("-n", type=int, default=5)
    a = sub.add_parser("add")
    a.add_argument("category")
    a.add_argument("topic")
    a.add_argument("content")
    a.add_argument("-i", "--importance", type=int, default=3)
    u = sub.add_parser("update")
    u.add_argument("id", type=int)
    u.add_argument("content")
    d = sub.add_parser("delete")
    d.add_argument("id", type=int)
    sub.add_parser("topics")
    args = p.parse_args()

    conn = connect()
    with conn:
        if args.cmd == "search":
            q = fts_query(args.query)
            rows = conn.execute(
                "select rowid, category, topic, content, importance, updated_at from memories "
                "where memories match ? order by rank - importance * 0.5 limit ?",
                (q, args.n),
            ).fetchall() if q else []
            show(rows)
        elif args.cmd == "add":
            cur = conn.execute(
                "insert into memories values (?, ?, ?, ?, ?)",
                (args.category, args.topic, args.content, args.importance, now()),
            )
            print(f"saved #{cur.lastrowid}")
        elif args.cmd == "update":
            n = conn.execute(
                "update memories set content = ?, updated_at = ? where rowid = ?",
                (args.content, now(), args.id),
            ).rowcount
            print(f"updated #{args.id}" if n else "not found")
        elif args.cmd == "delete":
            n = conn.execute("delete from memories where rowid = ?", (args.id,)).rowcount
            print(f"deleted #{args.id}" if n else "not found")
        elif args.cmd == "topics":
            rows = conn.execute(
                "select category, topic, count(*) from memories group by category, topic order by category, topic"
            ).fetchall()
            for category, topic, count in rows:
                print(f"{category}/{topic}: {count}")
            if not rows:
                print("empty")


if __name__ == "__main__":
    main()
