import os
import sqlite3
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-before-production")
DB_PATH = os.environ.get("DB_PATH", "bookings.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                service TEXT NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("customer_name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        service = request.form.get("service", "").strip()
        appointment_date = request.form.get("appointment_date", "").strip()
        appointment_time = request.form.get("appointment_time", "").strip()
        message = request.form.get("message", "").strip()

        if not all([name, phone, service, appointment_date, appointment_time]):
            flash("Please complete all required fields.", "error")
            return redirect(url_for("home") + "#booking")

        with get_db() as conn:
            conn.execute(
                """INSERT INTO bookings
                (customer_name, phone, email, service, appointment_date, appointment_time, message)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (name, phone, email, service, appointment_date, appointment_time, message)
            )
        flash("Your appointment request has been received. We will contact you to confirm.", "success")
        return redirect(url_for("home") + "#booking")

    return render_template("index.html", today=date.today().isoformat())

@app.route("/admin")
def admin():
    # Simple demo dashboard. Add authentication before using this publicly.
    with get_db() as conn:
        bookings = conn.execute("SELECT * FROM bookings ORDER BY created_at DESC").fetchall()
    return render_template("admin.html", bookings=bookings)

@app.route("/health")
def health():
    return {"status": "ok"}

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
