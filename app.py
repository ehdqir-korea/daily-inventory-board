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
# Row 변환
# =========================
def row_to_dict(row):
    return dict(row) if row else None


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
        rows = conn.execute("""
            SELECT id, name, band, dept
            FROM workers
            ORDER BY dept, name
        """).fetchall()

    return jsonify([row_to_dict(r) for r in rows])


@app.route("/api/workers", methods=["POST"])
def add_worker():
    data = request.get_json()

    name = (data.get("name") or "").strip()
    band = (data.get("band") or "").strip()
    dept = (data.get("dept") or "").strip()

    if not name or not dept:
        return jsonify({"error": "이름과 부서는 필수입니다."}), 400

    with get_conn() as conn:
        conn.execute("""
            INSERT INTO workers (name, band, dept)
            VALUES (?, ?, ?)
        """, (name, band, dept))
        conn.commit()

    return jsonify({"ok": True})


@app.route("/api/workers/<int:worker_id>", methods=["DELETE"])
def delete_worker(worker_id):
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM workers WHERE id = ?",
            (worker_id,)
        )
        conn.commit()

    return jsonify({"ok": True})


# =========================
# leave (휴가)
# =========================
@app.route("/api/leaves", methods=["GET"])
def get_leaves():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT
                id,
                start_date AS startDate,
                end_date AS endDate,
                name,
                dept,
                band,
                type,
                note,
                image_data AS imageData,
                submitted_at AS submittedAt
            FROM leave_requests
            ORDER BY start_date DESC, id DESC
        """).fetchall()

    return jsonify([row_to_dict(r) for r in rows])


@app.route("/api/leaves", methods=["POST"])
def add_leave():
    data = request.get_json()

    with get_conn() as conn:
        conn.execute("""
            INSERT INTO leave_requests
            (
                start_date,
                end_date,
                name,
                dept,
                band,
                type,
                note,
                image_data,
                submitted_at
            )
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


@app.route("/api/leaves/<int:leave_id>", methods=["PUT"])
def update_leave(leave_id):
    data = request.get_json()

    with get_conn() as conn:
        conn.execute("""
            UPDATE leave_requests
            SET
                start_date = ?,
                end_date = ?,
                name = ?,
                dept = ?,
                band = ?,
                type = ?,
                note = ?,
                image_data = ?,
                submitted_at = ?
            WHERE id = ?
        """, (
            data.get("startDate"),
            data.get("endDate"),
            data.get("name"),
            data.get("dept"),
            data.get("band"),
            data.get("type"),
            data.get("note"),
            data.get("imageData"),
            data.get("submittedAt"),
            leave_id
        ))
        conn.commit()

    return jsonify({"ok": True})


@app.route("/api/leaves/<int:leave_id>", methods=["DELETE"])
def delete_leave(leave_id):
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM leave_requests WHERE id = ?",
            (leave_id,)
        )
        conn.commit()

    return jsonify({"ok": True})


# =========================
# overtime (연장근무)
# =========================
@app.route("/api/overtime", methods=["GET"])
def get_overtime():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT
                id,
                date,
                day_name AS dayName,
                dept,
                worker_name AS workerName,
                worker_band AS workerBand,
                absent_name AS absentName,
                absent_band AS absentBand,
                absence_type AS absenceType,
                note,
                image_data AS imageData,
                worker_role AS workerRole,
                absent_role AS absentRole,
                replacement_role AS replacementRole,
                sequence_no AS sequenceNo,
                total_work AS totalWork,
                overtime,
                overtime_hours AS overtimeHours,
                action_text AS actionText
            FROM overtime_history
            ORDER BY date DESC, id DESC
        """).fetchall()

    return jsonify([row_to_dict(r) for r in rows])


@app.route("/api/overtime", methods=["POST"])
def add_overtime():
    data = request.get_json()

    with get_conn() as conn:
        conn.execute("""
            INSERT INTO overtime_history
            (
                date,
                day_name,
                dept,
                worker_name,
                worker_band,
                absent_name,
                absent_band,
                absence_type,
                note,
                image_data,
                worker_role,
                absent_role,
                replacement_role,
                sequence_no,
                total_work,
                overtime,
                overtime_hours,
                action_text
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("date"),
            data.get("dayName"),
            data.get("dept"),
            data.get("workerName"),
            data.get("workerBand"),
            data.get("absentName"),
            data.get("absentBand"),
            data.get("absenceType"),
            data.get("note"),
            data.get("imageData"),
            data.get("workerRole"),
            data.get("absentRole"),
            data.get("replacementRole"),
            data.get("sequenceNo"),
            data.get("totalWork"),
            data.get("overtime"),
            data.get("overtimeHours"),
            data.get("actionText")
        ))
        conn.commit()

    return jsonify({"ok": True})


@app.route("/api/overtime/<int:item_id>", methods=["PUT"])
def update_overtime(item_id):
    data = request.get_json()

    with get_conn() as conn:
        conn.execute("""
            UPDATE overtime_history
            SET
                date = ?,
                day_name = ?,
                dept = ?,
                worker_name = ?,
                worker_band = ?,
                absent_name = ?,
                absent_band = ?,
                absence_type = ?,
                note = ?,
                image_data = ?,
                worker_role = ?,
                absent_role = ?,
                replacement_role = ?,
                sequence_no = ?,
                total_work = ?,
                overtime = ?,
                overtime_hours = ?,
                action_text = ?
            WHERE id = ?
        """, (
            data.get("date"),
            data.get("dayName"),
            data.get("dept"),
            data.get("workerName"),
            data.get("workerBand"),
            data.get("absentName"),
            data.get("absentBand"),
            data.get("absenceType"),
            data.get("note"),
            data.get("imageData"),
            data.get("workerRole"),
            data.get("absentRole"),
            data.get("replacementRole"),
            data.get("sequenceNo"),
            data.get("totalWork"),
            data.get("overtime"),
            data.get("overtimeHours"),
            data.get("actionText"),
            item_id
        ))
        conn.commit()

    return jsonify({"ok": True})


@app.route("/api/overtime/<int:item_id>", methods=["DELETE"])
def delete_overtime(item_id):
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM overtime_history WHERE id = ?",
            (item_id,)
        )
        conn.commit()

    return jsonify({"ok": True})


# =========================
# purchases (구매신청)
# =========================
@app.route("/api/purchases", methods=["GET"])
def get_purchases():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT
                id,
                date,
                applicant,
                item_name AS itemName,
                link,
                note,
                image_data AS imageData
            FROM purchases
            ORDER BY date DESC, id DESC
        """).fetchall()

    return jsonify([row_to_dict(r) for r in rows])


@app.route("/api/purchases", methods=["POST"])
def add_purchase():
    data = request.get_json()

    with get_conn() as conn:
        conn.execute("""
            INSERT INTO purchases
            (
                date,
                applicant,
                item_name,
                link,
                note,
                image_data
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data.get("date"),
            data.get("applicant"),
            data.get("itemName"),
            data.get("link"),
            data.get("note"),
            data.get("imageData")
        ))
        conn.commit()

    return jsonify({"ok": True})


@app.route("/api/purchases/<int:item_id>", methods=["DELETE"])
def delete_purchase(item_id):
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM purchases WHERE id = ?",
            (item_id,)
        )
        conn.commit()

    return jsonify({"ok": True})


# =========================
# 실행
# =========================
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
