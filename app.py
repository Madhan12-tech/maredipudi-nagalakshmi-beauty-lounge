
import os
import hmac
import sqlite3
from functools import wraps
from datetime import date

from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, Response
)

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "change-this-before-deployment")

DATABASE = os.environ.get("DATABASE_PATH", "bookings.db")


# --------------------------------
# DATABASE CONNECTION
# --------------------------------

def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db()

    connection.execute("""
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

    connection.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            review_text TEXT NOT NULL,
            approved INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


init_db()


# --------------------------------
# ADMIN AUTHENTICATION
# --------------------------------

def admin_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):

        username = os.environ.get("ADMIN_USERNAME")
        password = os.environ.get("ADMIN_PASSWORD")

        if not username or not password:
            return "Admin credentials are not configured.", 503

        auth = request.authorization

        if (
            not auth
            or not hmac.compare_digest(auth.username or "", username)
            or not hmac.compare_digest(auth.password or "", password)
        ):
            return Response(
                "Admin login required.",
                401,
                {"WWW-Authenticate": 'Basic realm="Beauty Lounge Admin"'}
            )

        return function(*args, **kwargs)

    return decorated_function


# --------------------------------
# HOME PAGE
# --------------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        customer_name = request.form.get("customer_name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        service = request.form.get("service", "").strip()
        appointment_date = request.form.get("appointment_date", "").strip()
        appointment_time = request.form.get("appointment_time", "").strip()
        message = request.form.get("message", "").strip()

        if not all([
            customer_name, phone, service,
            appointment_date, appointment_time
        ]):
            flash("Please complete all required booking fields.", "error")
            return redirect(url_for("home") + "#booking")

        if len(customer_name) > 100 or len(message) > 1000:
            flash("Some entered information is too long.", "error")
            return redirect(url_for("home") + "#booking")

        if not phone.isdigit() or len(phone) != 10:
            flash("Please enter a valid 10-digit mobile number.", "error")
            return redirect(url_for("home") + "#booking")

        try:
            selected_date = date.fromisoformat(appointment_date)

            if selected_date < date.today():
                flash("Please choose today or a future appointment date.", "error")
                return redirect(url_for("home") + "#booking")

        except ValueError:
            flash("Please select a valid appointment date.", "error")
            return redirect(url_for("home") + "#booking")

        connection = get_db()

        connection.execute("""
            INSERT INTO bookings (
                customer_name,
                phone,
                email,
                service,
                appointment_date,
                appointment_time,
                message
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            customer_name,
            phone,
            email,
            service,
            appointment_date,
            appointment_time,
            message
        ))

        connection.commit()
        connection.close()

        flash(
            "Your appointment request has been received. "
            "We will contact you to confirm it.",
            "success"
        )

        return redirect(url_for("home") + "#booking")

    connection = get_db()

    reviews = connection.execute("""
        SELECT * FROM reviews
        WHERE approved = 1
        ORDER BY created_at DESC
    """).fetchall()

    connection.close()

    return render_template(
        "index.html",
        reviews=reviews,
        today=date.today().isoformat()
    )


# --------------------------------
# CUSTOMER REVIEW SUBMISSION
# --------------------------------

@app.route("/review", methods=["POST"])
def submit_review():

    customer_name = request.form.get("customer_name", "").strip()
    rating = request.form.get("rating", "").strip()
    review_text = request.form.get("review_text", "").strip()

    if not customer_name or not review_text:
        flash("Please enter your name and feedback.", "error")
        return redirect(url_for("home") + "#feedback")

    if len(customer_name) > 100 or len(review_text) > 1000:
        flash("Your feedback is too long.", "error")
        return redirect(url_for("home") + "#feedback")

    try:
        rating_value = int(rating)
    except (TypeError, ValueError):
        rating_value = 0

    if rating_value < 1 or rating_value > 5:
        flash("Please select a rating between 1 and 5.", "error")
        return redirect(url_for("home") + "#feedback")

    connection = get_db()

    connection.execute("""
        INSERT INTO reviews (
            customer_name,
            rating,
            review_text,
            approved
        )
        VALUES (?, ?, ?, 0)
    """, (customer_name, rating_value, review_text))

    connection.commit()
    connection.close()

    flash("Thank you! Your feedback was submitted for review.", "success")

    return redirect(url_for("home") + "#feedback")


# --------------------------------
# ADMIN DASHBOARD
# --------------------------------

@app.route("/admin")
@admin_required
def admin():

    connection = get_db()

    bookings = connection.execute("""
        SELECT * FROM bookings
        ORDER BY created_at DESC
    """).fetchall()

    reviews = connection.execute("""
        SELECT * FROM reviews
        ORDER BY created_at DESC
    """).fetchall()

    connection.close()

    return render_template(
        "admin.html",
        bookings=bookings,
        reviews=reviews
    )


# --------------------------------
# APPROVE CUSTOMER REVIEW
# --------------------------------

@app.route("/admin/review/<int:review_id>/approve", methods=["POST"])
@admin_required
def approve_review(review_id):

    connection = get_db()

    connection.execute("""
        UPDATE reviews
        SET approved = 1
        WHERE id = ?
    """, (review_id,))

    connection.commit()
    connection.close()

    flash("Review approved successfully.", "success")

    return redirect(url_for("admin"))


# --------------------------------
# DELETE CUSTOMER REVIEW
# --------------------------------

@app.route("/admin/review/<int:review_id>/delete", methods=["POST"])
@admin_required
def delete_review(review_id):

    connection = get_db()

    connection.execute("""
        DELETE FROM reviews
        WHERE id = ?
    """, (review_id,))

    connection.commit()
    connection.close()

    flash("Review deleted.", "success")

    return redirect(url_for("admin"))


# --------------------------------
# HEALTH CHECK FOR RENDER
# --------------------------------

@app.route("/health")
def health():
    return {"status": "healthy"}, 200


# --------------------------------
# LOCAL DEVELOPMENT
# --------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
