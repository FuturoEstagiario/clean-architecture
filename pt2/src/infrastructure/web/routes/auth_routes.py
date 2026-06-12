from flask import Blueprint, current_app, redirect, render_template, request, session

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET"])
def pagina():
    if "usuario" in session:
        return redirect("/")
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def entrar():
    login = request.form.get("login", "")
    senha = request.form.get("senha", "")
    res = current_app.container.auth_controller.autenticar(login, senha)
    if res["status"] == "sucesso":
        session["usuario"] = res["dados"]
        return redirect("/")
    return render_template("login.html", erro=res["mensagem"]), 401

@auth_bp.route("/logout", methods=["POST"])
def sair():
    session.clear()
    return redirect("/login")
