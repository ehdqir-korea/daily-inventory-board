DROP TABLE IF EXISTS workers;
DROP TABLE IF EXISTS leave_requests;
DROP TABLE IF EXISTS overtime_history;
DROP TABLE IF EXISTS purchases;

CREATE TABLE workers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  band TEXT,
  dept TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE leave_requests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  start_date TEXT NOT NULL,
  end_date TEXT NOT NULL,
  name TEXT NOT NULL,
  dept TEXT NOT NULL,
  band TEXT NOT NULL,
  type TEXT NOT NULL,
  note TEXT,
  image_data TEXT,
  submitted_at TEXT
);

CREATE TABLE overtime_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL,
  day_name TEXT,
  dept TEXT,
  worker_name TEXT NOT NULL,
  worker_band TEXT,
  absent_name TEXT,
  absent_band TEXT,
  absence_type TEXT,
  note TEXT,
  image_data TEXT,
  worker_role TEXT,
  absent_role TEXT,
  replacement_role TEXT,
  sequence_no TEXT,
  total_work TEXT,
  overtime TEXT,
  overtime_hours REAL,
  action_text TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE purchases (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL,
  applicant TEXT NOT NULL,
  item_name TEXT NOT NULL,
  link TEXT,
  note TEXT,
  image_data TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
