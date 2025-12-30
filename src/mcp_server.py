import sqlite3
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("users")

DB_PATH = "data/app.db"


@mcp.tool()
def search_users(query: str) -> list[dict[str, str | int]]:
    """Search users by name or email (partial match)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, email FROM users WHERE name LIKE ? OR email LIKE ?",
        (f"%{query}%", f"%{query}%"),
    )
    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": row["id"], "name": row["name"], "email": row["email"]} for row in rows
    ]


if __name__ == "__main__":
    mcp.run()
