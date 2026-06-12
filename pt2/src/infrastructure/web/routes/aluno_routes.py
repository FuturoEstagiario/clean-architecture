from flask import Blueprint, current_app, jsonify, render_template, request

aluno_bp = Blueprint("aluno", __name__)

@aluno_bp.route("/alunos", methods=["GET"])
def pagina():
    return render_template("alunos.html")

@aluno_bp.route("/api/alunos", methods=["POST"])
def cadastrar():
    data = request.get_json(silent=True)
    if not data or "matricula" not in data or "nome" not in data:
        return jsonify({"status": "erro", "mensagem": "Matrícula e nome são obrigatórios."}), 400

    res = current_app.container.aluno_controller.cadastrar(data["matricula"], data["nome"])
    if res["status"] == "sucesso":
        return jsonify(res), 201
    return jsonify(res), 400

@aluno_bp.route("/api/alunos", methods=["GET"])
def listar():
    return jsonify(current_app.container.aluno_controller.listar()), 200
