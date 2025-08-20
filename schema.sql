PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS operators (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS production_orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_code TEXT NOT NULL,
  quantity INTEGER NOT NULL,
  due_date TEXT,
  status TEXT NOT NULL DEFAULT 'scheduled', -- scheduled | in_progress | completed | on_hold | cancelled
  assigned_operator_id INTEGER,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (assigned_operator_id) REFERENCES operators(id)
);
