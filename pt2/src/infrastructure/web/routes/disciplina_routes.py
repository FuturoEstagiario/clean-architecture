from flask import Blueprint, current_app, jsonify, render_template, request

disciplina_bp = Blueprint("disciplina", __name__)

@disciplina_bp.route("/disciplinas", methods=["GET"])
def pagina():
    return render_template("disciplinas.html")

@disciplina_bp.route("/api/disciplinas", methods=["POST"])
def cadastrar():
    data = request.get_json(silent=True)
    if not data or "codigo" not in data or "nome" not in data or "carga_horaria" not in data:
        return jsonify({"status": "erro", "mensagem": "Código, nome e carga_horaria são obrigatórios."}), 400

    try:
        carga_horaria = int(data["carga_horaria"])
    except (TypeError, ValueError):
        return jsonify({"status": "erro", "mensagem": "Carga horária deve ser um número inteiro."}), 400

    res = current_app.container.disciplina_controller.cadastrar(data["codigo"], data["nome"], carga_horaria)
    if res["status"] == "sucesso":
        return jsonify(res), 201
    return jsonify(res), 400

@disciplina_bp.route("/api/disciplinas", methods=["GET"])
def listar():
    return jsonify(current_app.container.disciplina_controller.listar()), 200
