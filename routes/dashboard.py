from flask import Blueprint, render_template
from database.db import get_connection

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
def dashboard():

    conn = get_connection()
    cur = conn.cursor()

    # ==========================
    # Total Customers
    # ==========================
    cur.execute("SELECT COUNT(*) FROM customers")
    total_customers = cur.fetchone()[0]

    # ==========================
    # Total Products
    # ==========================
    cur.execute("SELECT COUNT(*) FROM products")
    total_products = cur.fetchone()[0]

    # ==========================
    # Total Sales
    # ==========================
    cur.execute("SELECT COUNT(*) FROM sales")
    total_sales = cur.fetchone()[0]

    # ==========================
    # Total Revenue
    # ==========================
    cur.execute("""
        SELECT COALESCE(SUM(total_amount), 0)
        FROM sales
    """)
    total_revenue = cur.fetchone()[0]

    # ==========================
    # Total Profit
    # ==========================
    cur.execute("""
        SELECT COALESCE(SUM(profit), 0)
        FROM sales
    """)
    total_profit = cur.fetchone()[0]

    # ==========================
    # Monthly Sales Chart
    # ==========================
    cur.execute("""
        SELECT
            TO_CHAR(sale_date, 'Mon') AS month,
            SUM(total_amount) AS total
        FROM sales
        GROUP BY
            EXTRACT(MONTH FROM sale_date),
            TO_CHAR(sale_date, 'Mon')
        ORDER BY
            EXTRACT(MONTH FROM sale_date)
    """)

    chart_data = cur.fetchall()

    months = []
    sales = []

    for row in chart_data:
        months.append(row[0])
        sales.append(float(row[1]))

    cur.close()
    conn.close()

    return render_template(
        "dashboard.html",
        total_customers=total_customers,
        total_products=total_products,
        total_sales=total_sales,
        total_revenue=total_revenue,
        total_profit=total_profit,
        months=months,
        sales=sales
    )