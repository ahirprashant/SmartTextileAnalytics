from flask import Blueprint, render_template, request, redirect, flash
from database.db import get_connection

products_bp = Blueprint("products", __name__)

# ==========================
# View Products
# ==========================
@products_bp.route("/products")
def products():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            product_id,
            product_name,
            category,
            brand,
            fabric,
            cost_price,
            selling_price,
            gst
        FROM products
        ORDER BY product_id
        LIMIT 100
    """)

    products = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "products.html",
        products=products
    )


# ==========================
# Add Product
# ==========================
@products_bp.route("/products/add", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        product_name = request.form["product_name"]
        category = request.form["category"]
        brand = request.form["brand"]
        fabric = request.form["fabric"]
        cost_price = request.form["cost_price"]
        selling_price = request.form["selling_price"]
        gst = request.form["gst"]

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO products
            (
                product_name,
                category,
                brand,
                fabric,
                cost_price,
                selling_price,
                gst
            )
            VALUES
            (%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            product_name,
            category,
            brand,
            fabric,
            cost_price,
            selling_price,
            gst
        ))

        conn.commit()

        cur.close()
        conn.close()

        flash("Product Added Successfully.", "success")

        return redirect("/products")

    return render_template("add_product.html")
# ==========================
# Edit Product
# ==========================
@products_bp.route("/products/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":

        product_name = request.form["product_name"]
        category = request.form["category"]
        brand = request.form["brand"]
        fabric = request.form["fabric"]
        cost_price = request.form["cost_price"]
        selling_price = request.form["selling_price"]
        gst = request.form["gst"]

        cur.execute("""
            UPDATE products
            SET
                product_name=%s,
                category=%s,
                brand=%s,
                fabric=%s,
                cost_price=%s,
                selling_price=%s,
                gst=%s
            WHERE product_id=%s
        """,
        (
            product_name,
            category,
            brand,
            fabric,
            cost_price,
            selling_price,
            gst,
            id
        ))

        conn.commit()

        cur.close()
        conn.close()

        flash("Product Updated Successfully.", "success")

        return redirect("/products")

    cur.execute("""
        SELECT
            product_id,
            product_name,
            category,
            brand,
            fabric,
            cost_price,
            selling_price,
            gst
        FROM products
        WHERE product_id=%s
    """, (id,))

    product = cur.fetchone()

    cur.close()
    conn.close()

    return render_template(
        "edit_product.html",
        product=product
    )
# ==========================
# Delete Product
# ==========================
@products_bp.route("/products/delete/<int:id>")
def delete_product(id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            "DELETE FROM products WHERE product_id=%s",
            (id,)
        )

        conn.commit()

        flash(
            "Product Deleted Successfully.",
            "success"
        )

    except Exception:

        conn.rollback()

        flash(
            "Product cannot be deleted because it is used in other records.",
            "danger"
        )

    finally:

        cur.close()
        conn.close()

    return redirect("/products")