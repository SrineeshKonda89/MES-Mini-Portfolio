import sqlite3
from contextlib import closing

DB_PATH = "mes.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with closing(get_conn()) as conn, open("schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
        conn.commit()

def list_operators():
    with closing(get_conn()) as conn:
        return conn.execute("SELECT id, name FROM operators ORDER BY name").fetchall()

def add_operator(name: str):
    with closing(get_conn()) as conn:
        conn.execute("INSERT OR IGNORE INTO operators(name) VALUES (?)", (name,))
        conn.commit()

def create_order(product_code: str, quantity: int, due_date: str | None):
    with closing(get_conn()) as conn:
        conn.execute(
            "INSERT INTO production_orders(product_code, quantity, due_date) VALUES (?, ?, ?)",
            (product_code, quantity, due_date),
        )
        conn.commit()

def list_orders(status_filter: str | None = None):
    q = "SELECT po.*, op.name as operator_name FROM production_orders po LEFT JOIN operators op ON op.id = po.assigned_operator_id"
    params = ()
    if status_filter and status_filter != "all":
        q += " WHERE po.status = ?"
        params = (status_filter,)
    q += " ORDER BY po.created_at DESC"
    with closing(get_conn()) as conn:
        return conn.execute(q, params).fetchall()

def update_order_status(order_id: int, status: str):
    with closing(get_conn()) as conn:
        conn.execute(
            "UPDATE production_orders SET status=?, updated_at=datetime('now') WHERE id=?",
            (status, order_id),
        )
        conn.commit()

def assign_operator(order_id: int, operator_id: int | None):
    with closing(get_conn()) as conn:
        conn.execute(
            "UPDATE production_orders SET assigned_operator_id=?, updated_at=datetime('now') WHERE id=?",
            (operator_id, order_id),
        )
        conn.commit()
