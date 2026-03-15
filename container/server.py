"""
MCP server exposing read-only tools over a SQLite car database.
"""

import os
import sqlite3
from contextlib import contextmanager
from typing import Generator

from mcp.server.fastmcp import FastMCP

DB_PATH = os.environ.get("DB_PATH", "cars.db")

mcp = FastMCP("cars-demo")


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def list_manufacturers(country: str | None = None) -> list[dict]:
    """
    Return all car manufacturers.

    Args:
        country: Optional country filter (e.g. 'Japan', 'USA', 'Germany').
    """
    with get_db() as conn:
        if country:
            rows = conn.execute(
                "SELECT id, name, country, founded FROM manufacturers WHERE country = ? ORDER BY name",
                (country,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, name, country, founded FROM manufacturers ORDER BY name"
            ).fetchall()
        return [dict(row) for row in rows]


@mcp.tool()
def list_models(
    manufacturer_id: int | None = None,
    category: str | None = None,
    in_production: bool | None = None,
) -> list[dict]:
    """
    Return car models with optional filters.

    Args:
        manufacturer_id: Filter by manufacturer ID.
        category: Filter by body style — one of: sedan, suv, truck, sports, van.
        in_production: If True, return only models still in production (year_end is NULL).
                       If False, return only discontinued models.
    """
    query = """
        SELECT m.id, m.name, mfr.name AS manufacturer, m.year_start, m.year_end, m.category
        FROM models m
        JOIN manufacturers mfr ON mfr.id = m.manufacturer_id
        WHERE 1=1
    """
    params: list = []

    if manufacturer_id is not None:
        query += " AND m.manufacturer_id = ?"
        params.append(manufacturer_id)
    if category:
        query += " AND m.category = ?"
        params.append(category)
    if in_production is True:
        query += " AND m.year_end IS NULL"
    elif in_production is False:
        query += " AND m.year_end IS NOT NULL"

    query += " ORDER BY mfr.name, m.name"

    with get_db() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]


@mcp.tool()
def get_model(model_id: int) -> dict | None:
    """
    Return details for a single car model, including its manufacturer.

    Args:
        model_id: The model ID.
    """
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT m.id, m.name, mfr.name AS manufacturer, mfr.country,
                   m.year_start, m.year_end, m.category
            FROM models m
            JOIN manufacturers mfr ON mfr.id = m.manufacturer_id
            WHERE m.id = ?
            """,
            (model_id,),
        ).fetchone()
        return dict(row) if row else None


@mcp.tool()
def list_parts(
    model_id: int | None = None,
    category: str | None = None,
) -> list[dict]:
    """
    Return parts with optional filters.

    Args:
        model_id: Filter by model ID.
        category: Filter by part category — one of: engine, suspension, brakes,
                  electrical, body, interior.
    """
    query = """
        SELECT p.id, p.part_number, p.name, p.category, p.description,
               m.name AS model, mfr.name AS manufacturer
        FROM parts p
        JOIN models m ON m.id = p.model_id
        JOIN manufacturers mfr ON mfr.id = m.manufacturer_id
        WHERE 1=1
    """
    params: list = []

    if model_id is not None:
        query += " AND p.model_id = ?"
        params.append(model_id)
    if category:
        query += " AND p.category = ?"
        params.append(category)

    query += " ORDER BY mfr.name, m.name, p.category, p.name"

    with get_db() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]


@mcp.tool()
def search_parts(keyword: str) -> list[dict]:
    """
    Search for parts whose name or description contains the given keyword (case-insensitive).

    Args:
        keyword: Search term to match against part name and description.
    """
    pattern = f"%{keyword}%"
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT p.id, p.part_number, p.name, p.category, p.description,
                   m.name AS model, mfr.name AS manufacturer
            FROM parts p
            JOIN models m ON m.id = p.model_id
            JOIN manufacturers mfr ON mfr.id = m.manufacturer_id
            WHERE p.name LIKE ? OR p.description LIKE ?
            ORDER BY mfr.name, m.name, p.name
            """,
            (pattern, pattern),
        ).fetchall()
        return [dict(row) for row in rows]


@mcp.tool()
def get_part(part_id: int) -> dict | None:
    """
    Return full details for a single part.

    Args:
        part_id: The part ID.
    """
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT p.id, p.part_number, p.name, p.category, p.description,
                   m.id AS model_id, m.name AS model,
                   mfr.id AS manufacturer_id, mfr.name AS manufacturer
            FROM parts p
            JOIN models m ON m.id = p.model_id
            JOIN manufacturers mfr ON mfr.id = m.manufacturer_id
            WHERE p.id = ?
            """,
            (part_id,),
        ).fetchone()
        return dict(row) if row else None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mcp.streamable_http_app(), host="0.0.0.0", port=8000)
