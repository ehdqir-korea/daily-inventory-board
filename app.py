from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "overtime.db"


# =========================
# DB 연결
# =========================
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# DB 초기화
# =========================
def init_db():
    if not os.path.exists(DB_PATH):
        with get_conn() as conn:
            with open("schema.sql", "r", encoding="utf-8") as f:
                conn.executescript(f.read())
            conn.commit()


# =========================
# HTML 로딩
# =========================
@app.route("/")
def index():
    return send_from_directory(".", "Overtime.html")


# =========================
# workers
# =========================
@app.route("/api/workers", methods=["GET"])
def get_workers():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM workers").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/workers", methods=["POST"])
def add_worker():
    data = request.get_json()

    with get_conn() as conn:
        conn.execute("""
            INSERT INTO workers (name, band, dept)
            VALUES (?, ?, ?)
        """, (
            data.get("name"),
            data.get("band"),
            data.get("dept")
        ))
        conn.commit()

    return jsonify({"ok": True})


# =========================
# leave (휴가)
# =========================
@app.route("/api/leaves", methods=["GET"])
def get_leaves():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM leave_requests").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/leaves", methods=["POST"])
def add_leave():
    data = request.get_json()

    with get_conn() as conn:
        conn.execute("""
            INSERT INTO leave_requests
            (start_date, end_date, name, dept, band, type, note, image_data, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("startDate"),
            data.get("endDate"),
            data.get("name"),
            data.get("dept"),
            data.get("band"),
            data.get("type"),
            data.get("note"),
            data.get("imageData"),
            data.get("submittedAt")
        ))
        conn.commit()

    return jsonify({"ok": True})


# =========================
# overtime (연장근무)
# =========================
@app.route("/api/overtime", methods=["GET"])
def get_overtime():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM overtime_history").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/overtime", methods=["POST"])
def add_overtime():
    data = request.get_json()

    with get_conn() as conn:
        conn.execute("""
            INSERT INTO overtime_history
            (date, worker_name, absent_name, absence_type, total_work, overtime, overtime_hours)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("date"),
            data.get("workerName"),
            data.get("absentName"),
            data.get("absenceType"),
            data.get("totalWork"),
            data.get("overtime"),
            data.get("overtimeHours")
        ))
        conn.commit()

    return jsonify({"ok": True})


# =========================
# purchase (구매)
# =========================
@app.route("/api/purchases", methods=["GET"])
def get_purchases():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM purchases").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/purchases", methods=["POST"])
def add_purchase():
    data = request.get_json()

    with get_conn() as conn:
        conn.execute("""
            INSERT INTO purchases
            (date, applicant, item_name, link, note)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data.get("date"),
            data.get("applicant"),
            data.get("itemName"),
            data.get("link"),
            data.get("note")
        ))
        conn.commit()

    return jsonify({"ok": True})


# =========================
# 실행
# =========================
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
