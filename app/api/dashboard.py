from flask import Blueprint, session, redirect, render_template


dash_bp=Blueprint('dashboard',__name__)
@dash_bp.route("/dashboard")

def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        user=session
    )