from flask import Blueprint, render_template, request, redirect, flash
from database.db import get_connection

sales_bp = Blueprint("sales", __name__)


# ==========================================
# View Sales
# ==========================================
@sales_bp.route("/sales")
def sales():

    conn = get_connection()
    cur = conn.cursor()

    search = request.args.get("search", "")
    from_date = request.args.get("from_date", "")
    to_date = request.args.get("to_date", "")

    query = """
    SELECT
        s.sale_id,
        c.customer_name,
        p.product_name,
        s.quantity,
        s.unit_price,
        s.total_amount,
        s.profit,
        s.payment_method,
        s.sale_date
    FROM sales s
    JOIN customers c
        ON s.customer_id = c.customer_id
    JOIN products p
        ON s.product_id = p.product_id
    WHERE 1=1
    """

    params = []

    if search:
        query += """
        AND (
            c.customer_name ILIKE %s
            OR p.product_name ILIKE %s
        )
        """
        params.extend([
            f"%{search}%",
            f"%{search}%"
        ])

    if from_date:
        query += " AND s.sale_date >= %s"
        params.append(from_date)

    if to_date:
        query += " AND s.sale_date <= %s"
        params.append(to_date)

    query += """
    ORDER BY s.sale_id DESC
    LIMIT 100
    """

    cur.execute(query, tuple(params))

    sales = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "sales.html",
        sales=sales,
        search=search,
        from_date=from_date,
        to_date=to_date
    )


# ==========================================
# Add Sale
# ==========================================
@sales_bp.route("/sales/add", methods=["GET", "POST"])
def add_sale():

    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":

        customer_id = request.form["customer_id"]
        product_id = request.form["product_id"]
        quantity = int(request.form["quantity"])
        payment_method = request.form["payment_method"]

        # Product Details
        cur.execute("""
            SELECT
                cost_price,
                selling_price,
                gst
            FROM products
            WHERE product_id=%s
        """, (product_id,))

        product = cur.fetchone()

        if product is None:

            flash("Product Not Found", "danger")

            cur.close()
            conn.close()

            return redirect("/sales/add")

        cost_price = float(product[0])
        selling_price = float(product[1])
        gst = float(product[2])

        unit_price = selling_price
        discount = 0

        subtotal = quantity * unit_price
        gst_amount = subtotal * gst / 100
        total_amount = subtotal + gst_amount

        profit = (selling_price - cost_price) * quantity

        cur.execute("""
        INSERT INTO sales
        (
            customer_id,
            product_id,
            quantity,
            unit_price,
            cost_price,
            discount,
            gst,
            total_amount,
            profit,
            payment_method,
            sale_date
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_DATE
        )
        """,
        (
            customer_id,
            product_id,
            quantity,
            unit_price,
            cost_price,
            discount,
            gst,
            total_amount,
            profit,
            payment_method
        ))

        conn.commit()

        flash("Sale Added Successfully!", "success")

        cur.close()
        conn.close()

        return redirect("/sales")

    # ==========================
    # Customer Dropdown
    # ==========================
    cur.execute("""
        SELECT
            customer_id,
            customer_name
        FROM customers
        ORDER BY customer_name
    """)

    customers = cur.fetchall()

    # ==========================
    # Product Dropdown
    # ==========================
    cur.execute("""
        SELECT
            MIN(product_id),
            product_name,
            brand,
            fabric
        FROM products
        GROUP BY
            product_name,
            brand,
            fabric
        ORDER BY
            product_name,
            brand
    """)

    products = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "add_sale.html",
        customers=customers,
        products=products
    )