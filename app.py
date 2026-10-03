"""
app.py — standalone test runner for the admin panel branch.

This is NOT the team's main app.py. It exists only so you can run and
demo the admin panel on its own, before the branches are merged.

Once feature/admin-panel is merged into main, the team's real app.py
should just add:

    from admin import admin_bp
    app.register_blueprint(admin_bp)

...and this file can be deleted.

Run it with:
    pip install flask
    python app.py

Then open: http://127.0.0.1:5000/admin/login
Login with username: admin   password: admin123
"""

from flask import Flask, redirect, url_for
from admin import admin_bp

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-this-before-deployment"  # needed for session/flash

app.register_blueprint(admin_bp)


@app.route("/")
def home():
    return redirect(url_for("admin.admin_login"))


if __name__ == "__main__":
    app.run(debug=True)
