from flask import Blueprint, render_template, session, redirect
from app.db.user_repo import user_repo

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():

    # User not logged in
    if "user_id" not in session:
        return redirect("/login")

    # Fetch user from database
    user = user_repo.get_user_by_user_id(session["user_id"])

    if user is None:
        session.clear()
        return redirect("/login")

    return render_template(
        "dashboard.html",
        user=user
    )