
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
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
                review_text TEXT NOT NULL,
                approved INTEGER NOT NULL DEFAULT 0,
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

    with get_db() as conn:
        reviews = conn.execute(
            "SELECT customer_name, rating, review_text, created_at FROM reviews WHERE approved = 1 ORDER BY created_at DESC LIMIT 12"
        ).fetchall()
    return render_template("index.html", today=date.today().isoformat(), reviews=reviews)


@app.route("/review", methods=["POST"])
def submit_review():
    name = request.form.get("review_name", "").strip()
    rating = request.form.get("rating", "").strip()
    review_text = request.form.get("review_text", "").strip()

    try:
        rating_value = int(rating)
    except (TypeError, ValueError):
        rating_value = 0

    if not name or len(name) > 100 or not review_text or len(review_text) > 1000 or rating_value not in range(1, 6):
        flash("Please enter your name, a rating from 1 to 5, and feedback (up to 1000 characters).", "error")
        return redirect(url_for("home") + "#reviews")

    with get_db() as conn:
        conn.execute(
            "INSERT INTO reviews (customer_name, rating, review_text) VALUES (?, ?, ?)",
            (name, rating_value, review_text)
        )

    flash("Thank you for your feedback! It will appear after salon approval.", "success")
    return redirect(url_for("home") + "#reviews")


@app.route("/admin")
def admin():
    # Demo dashboard only. Add authentication before making this route public.
    with get_db() as conn:
        bookings = conn.execute("SELECT * FROM bookings ORDER BY created_at DESC").fetchall()
        reviews = conn.execute("SELECT * FROM reviews ORDER BY created_at DESC").fetchall()
    return render_template("admin.html", bookings=bookings, reviews=reviews)


@app.route("/admin/review/<int:review_id>/approve", methods=["POST"])
def approve_review(review_id):
    # Protect /admin and this action with authentication before public launch.
    with get_db() as conn:
        conn.execute("UPDATE reviews SET approved = 1 WHERE id = ?", (review_id,))
    flash("Review approved.", "success")
    return redirect(url_for("admin"))


@app.route("/admin/review/<int:review_id>/delete", methods=["POST"])
def delete_review(review_id):
    # Protect /admin and this action with authentication before public launch.
    with get_db() as conn:
        conn.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    flash("Review deleted.", "success")
    return redirect(url_for("admin"))


@app.route("/health")
def health():
    return {"status": "ok"}


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
