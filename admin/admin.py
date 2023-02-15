from flask import Blueprint, request, render_template, url_for, redirect, flash, session


admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


def login_admin():
    session["admin_logged"] = 1


def is_logged():
    return True if session.get("admin_logged") else False


def logout_admin():
    session.pop("admin_logged", None)


@admin.route("/")
def index():
    if not is_logged():
        return redirect(url_for(".login"))
    
    return render_template("admin/index.html", title="Adm")


@admin.route("/login", methods=["POST", "GET"])
def login():
    if not is_logged():
        return redirect(url_for(".index"))
    
    if request.method == "POST":
        if request.form["user"] == "admin" and request.form["psw"] == "123":
            login_admin()
            return redirect(url_for(".index"))
        else:
            flash("Error", "danger")
            
    return render_template("admin/login.html", title="Adm")


@admin.route("/logout", methods=["POST", "GET"])
def logout():
    if not is_logged():
        return redirect(url_for(".login"))
    
    logout_admin()
    
    return redirect(url_for(".login"))
