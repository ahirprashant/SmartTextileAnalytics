from flask import Blueprint, render_template, request, redirect, flash
from database.db import get_connection

inventory_bp = Blueprint("inventory", __name__)


# ==========================================
# Inventory List
# ==========================================
@inventory_bp.route("/inventory")
def inventory():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            i.inventory_id,
            p.product_name,
            p.brand,
            i.stock,
            i.reorder_level,
            i.warehouse
        FROM inventory i
        JOIN products p
            ON i.product_id = p.product_id
        ORDER BY p.product_name
    """)

    inventory = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "inventory.html",
        inventory=inventory
    )


# ==========================================
# Add Inventory
# ==========================================
@inventory_bp.route("/add_inventory", methods=["GET", "POST"])
def add_inventory():

    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":

        product_id = int(request.form["product_id"])
        stock = int(request.form["stock"])
        reorder_level = int(request.form["reorder_level"])
        warehouse = request.form["warehouse"]

        # Check Product Already Exists
        cur.execute("""
    SELECT
        MIN(product_id) AS product_id,
        product_name,
        brand
    FROM products
    GROUP BY product_name, brand
    ORDER BY product_name
""")

        check = cur.fetchone()

        # Product Exists -> Update Stock
        if check:

            cur.execute("""
                UPDATE inventory
                SET
                    stock = stock + %s,
                    reorder_level = %s,
                    warehouse = %s
                WHERE product_id = %s
            """, (
                stock,
                reorder_level,
                warehouse,
                product_id
            ))

            conn.commit()

            flash("Stock Updated Successfully", "success")

            cur.close()
            conn.close()

            return redirect("/inventory")

        # New Product
        cur.execute("""
            INSERT INTO inventory
            (
                product_id,
                stock,
                reorder_level,
                warehouse
            )
            VALUES
            (%s,%s,%s,%s)
        """, (
            product_id,
            stock,
            reorder_level,
            warehouse
        ))

        conn.commit()

        flash("Inventory Added Successfully", "success")

        cur.close()
        conn.close()

        return redirect("/inventory")

    # Product Dropdown
    cur.execute("""
        SELECT
            product_id,
            product_name,
            brand
        FROM products
        ORDER BY product_name
    """)

    products = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "add_inventory.html",
        products=products
    )


# ==========================================
# Edit Inventory
# ==========================================
@inventory_bp.route("/edit_inventory/<int:id>", methods=["GET", "POST"])
def edit_inventory(id):

    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":

        stock = int(request.form["stock"])
        reorder_level = int(request.form["reorder_level"])
        warehouse = request.form["warehouse"]

        cur.execute("""
            UPDATE inventory
            SET
                stock=%s,
                reorder_level=%s,
                warehouse=%s
            WHERE inventory_id=%s
        """, (
            stock,
            reorder_level,
            warehouse,
            id
        ))

        conn.commit()

        flash("Inventory Updated Successfully", "success")

        cur.close()
        conn.close()

        return redirect("/inventory")

    cur.execute("""
        SELECT
            inventory_id,
            stock,
            reorder_level,
            warehouse
        FROM inventory
        WHERE inventory_id=%s
    """, (id,))

    inventory = cur.fetchone()

    cur.close()
    conn.close()

    return render_template(
        "edit_inventory.html",
        inventory=inventory
    )


# ==========================================
# Delete Inventory
# ==========================================
@inventory_bp.route("/delete_inventory/<int:id>")
def delete_inventory(id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM inventory
        WHERE inventory_id=%s
    """, (id,))

    conn.commit()

    flash("Inventory Deleted Successfully", "success")

    cur.close()
    conn.close()

    return redirect("/inventory")