DROP TABLE IF EXISTS workers;
DROP TABLE IF EXISTS leave_requests;
DROP TABLE IF EXISTS overtime_history;
DROP TABLE IF EXISTS purchases;

CREATE TABLE workers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  band TEXT,
  dept TEXT
);

CREATE TABLE leave_requests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  start_date TEXT,
  end_date TEXT,
  name TEXT,
  dept TEXT,
  band TEXT,
  type TEXT,
  note TEXT,
  image_data TEXT,
  submitted_at TEXT
);

CREATE TABLE overtime_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT,
  worker_name TEXT,
  absent_name TEXT,
  absence_type TEXT,
  total_work TEXT,
  overtime TEXT,
  overtime_hours REAL
);

CREATE TABLE purchases (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT,
  applicant TEXT,
  item_name TEXT,
  link TEXT,
  note TEXT
);
