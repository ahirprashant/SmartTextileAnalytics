from flask import Blueprint, render_template, request, redirect, flash
import psycopg2
from database.db import get_connection
from flask import Blueprint, render_template, request, redirect
from database.db import get_connection

customers_bp = Blueprint("customers", __name__)


# ==========================
# View Customers
# ==========================
@customers_bp.route("/customers")
def customers():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT customer_id,
               customer_name,
               mobile,
               email,
               city,
               customer_type,
               join_date
        FROM customers
        ORDER BY customer_id
        LIMIT 100
    """)

    customers = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "customers.html",
        customers=customers
    )


# ==========================
# Add Customer
# ==========================
@customers_bp.route("/customers/add", methods=["GET", "POST"])
def add_customer():

    if request.method == "POST":

        customer_name = request.form["customer_name"]
        mobile = request.form["mobile"]
        email = request.form["email"]
        city = request.form["city"]
        customer_type = request.form["customer_type"]

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO customers
            (customer_name, mobile, email, city, customer_type, join_date)
            VALUES (%s, %s, %s, %s, %s, CURRENT_DATE)
        """, (
            customer_name,
            mobile,
            email,
            city,
            customer_type
        ))

        conn.commit()

        cur.close()
        conn.close()

        return redirect("/customers")

    return render_template("add_customer.html")


# ==========================
# Edit Customer
# ==========================
@customers_bp.route("/customers/edit/<int:id>", methods=["GET", "POST"])
def edit_customer(id):

    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":

        customer_name = request.form["customer_name"]
        mobile = request.form["mobile"]
        email = request.form["email"]
        city = request.form["city"]
        customer_type = request.form["customer_type"]

        cur.execute("""
            UPDATE customers
            SET customer_name=%s,
                mobile=%s,
                email=%s,
                city=%s,
                customer_type=%s
            WHERE customer_id=%s
        """, (
            customer_name,
            mobile,
            email,
            city,
            customer_type,
            id
        ))

        conn.commit()

        cur.close()
        conn.close()

        return redirect("/customers")

    cur.execute("""
        SELECT customer_id,
               customer_name,
               mobile,
               email,
               city,
               customer_type
        FROM customers
        WHERE customer_id=%s
    """, (id,))

    customer = cur.fetchone()

    cur.close()
    conn.close()

    return render_template(
        "edit_customer.html",
        customer=customer
    )
@customers_bp.route("/customers/delete/<int:id>")
def delete_customer(id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            "DELETE FROM customers WHERE customer_id=%s",
            (id,)
        )

        conn.commit()

        flash("Customer deleted successfully.", "success")

    except psycopg2.Error:

        conn.rollback()

        flash(
            "Customer cannot be deleted because sales records exist.",
            "danger"
        )

    finally:

        cur.close()
        conn.close()

    return redirect("/customers")