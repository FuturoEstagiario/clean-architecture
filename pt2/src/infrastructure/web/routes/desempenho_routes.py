from flask import Blueprint, current_app, jsonify, render_template

desempenho_bp = Blueprint("desempenho", __name__)

@desempenho_bp.route("/desempenho", methods=["GET"])
def pagina():
    return render_template("desempenho.html")

@desempenho_bp.route("/api/desempenho/<matricula>", methods=["GET"])
def consultar(matricula):
    res = current_app.container.desempenho_controller.consultar_json(matricula)
    if res["status"] == "sucesso":
        return jsonify(res), 200
    return jsonify(res), 400
