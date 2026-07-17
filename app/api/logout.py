from flask import Blueprint, session, redirect

dash_bp=Blueprint('logout',__name__)
@dash_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/")