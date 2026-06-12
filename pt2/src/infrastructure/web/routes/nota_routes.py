from flask import Blueprint, current_app, jsonify, render_template, request

nota_bp = Blueprint("nota", __name__)

@nota_bp.route("/notas", methods=["GET"])
def pagina():
    return render_template("notas.html")

@nota_bp.route("/api/notas", methods=["POST"])
def lancar():
    data = request.get_json(silent=True)
    required = ["aluno_matricula", "disciplina_codigo", "valor", "tipo_avaliacao"]
    if not data or any(k not in data for k in required):
        return jsonify({"status": "erro", "mensagem": "Campos obrigatórios: aluno_matricula, disciplina_codigo, valor, tipo_avaliacao."}), 400

    try:
        valor = float(data["valor"])
    except (TypeError, ValueError):
        return jsonify({"status": "erro", "mensagem": "Valor da nota deve ser um número."}), 400

    res = current_app.container.nota_controller.lancar(
        data["aluno_matricula"], data["disciplina_codigo"], valor, data["tipo_avaliacao"]
    )
    if res["status"] == "sucesso":
        return jsonify(res), 201
    return jsonify(res), 400
