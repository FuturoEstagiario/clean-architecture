from flask import Blueprint, current_app, jsonify, render_template, request

matricula_bp = Blueprint("matricula", __name__)

@matricula_bp.route("/matriculas", methods=["GET"])
def pagina():
    return render_template("matriculas.html")

@matricula_bp.route("/api/matriculas", methods=["POST"])
def matricular():
    data = request.get_json(silent=True)
    if not data or "aluno_matricula" not in data or "disciplina_codigo" not in data:
        return jsonify({"status": "erro", "mensagem": "Matrícula do aluno e código da disciplina são obrigatórios."}), 400

    res = current_app.container.matricula_controller.matricular(data["aluno_matricula"], data["disciplina_codigo"])
    if res["status"] == "sucesso":
        return jsonify(res), 201
    return jsonify(res), 400

@matricula_bp.route("/api/matriculas", methods=["GET"])
def listar():
    return jsonify(current_app.container.matricula_controller.listar()), 200
