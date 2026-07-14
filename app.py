from flask import Flask, render_template

from routes.dashboard import dashboard_bp
from routes.customers import customers_bp
from routes.products import products_bp
from routes.sales import sales_bp

app = Flask(__name__)
app.secret_key = "smart_textile_analytics"

app.register_blueprint(dashboard_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(products_bp)
app.register_blueprint(sales_bp)


@app.route("/")
def login():
    return render_template("login.html")



if __name__ == "__main__":
    app.run(debug=True)