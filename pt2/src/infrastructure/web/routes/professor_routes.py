from flask import Blueprint, current_app, jsonify, render_template, request

professor_bp = Blueprint("professor", __name__)

@professor_bp.route("/professores", methods=["GET"])
def pagina():
    return render_template("professores.html")

@professor_bp.route("/api/professores", methods=["POST"])
def cadastrar():
    data = request.get_json(silent=True)
    if not data or "registro" not in data or "nome" not in data:
        return jsonify({"status": "erro", "mensagem": "Registro e nome são obrigatórios."}), 400

    res = current_app.container.professor_controller.cadastrar(data["registro"], data["nome"])
    if res["status"] == "sucesso":
        return jsonify(res), 201
    return jsonify(res), 400

@professor_bp.route("/api/professores", methods=["GET"])
def listar():
    return jsonify(current_app.container.professor_controller.listar()), 200
