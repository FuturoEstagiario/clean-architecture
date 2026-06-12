from flask import Blueprint, current_app, jsonify, render_template, request

frequencia_bp = Blueprint("frequencia", __name__)

@frequencia_bp.route("/frequencias", methods=["GET"])
def pagina():
    return render_template("frequencias.html")

@frequencia_bp.route("/api/frequencias", methods=["POST"])
def lancar():
    data = request.get_json(silent=True)
    required = ["aluno_matricula", "disciplina_codigo", "aulas_presente", "aulas_total"]
    if not data or any(k not in data for k in required):
        return jsonify({"status": "erro", "mensagem": "Campos obrigatórios: aluno_matricula, disciplina_codigo, aulas_presente, aulas_total."}), 400

    try:
        aulas_presente = int(data["aulas_presente"])
        aulas_total = int(data["aulas_total"])
    except (TypeError, ValueError):
        return jsonify({"status": "erro", "mensagem": "Aulas presente e total devem ser números inteiros."}), 400

    res = current_app.container.frequencia_controller.lancar(
        data["aluno_matricula"], data["disciplina_codigo"], aulas_presente, aulas_total
    )
    if res["status"] == "sucesso":
        return jsonify(res), 201
    return jsonify(res), 400
