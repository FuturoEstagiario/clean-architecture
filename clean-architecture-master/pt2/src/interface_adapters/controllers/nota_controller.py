from flask import Blueprint, request, jsonify
from src.application.use_cases.lancar_nota import LancarNota
from src.application.use_cases.consultar_desempenho import ConsultarDesempenho
from src.domain.entities.nota import NotaValorInvalidoError
from src.interface_adapters.repositories_impl.sqlite_nota_repository import SQLiteNotaRepository

nota_bp = Blueprint("nota", __name__)


@nota_bp.route("/notas", methods=["POST"])
def lancar_nota():
    data = request.get_json(silent=True) or {}
    matricula = str(data.get("matricula", "")).strip()
    disciplina = str(data.get("disciplina", "")).strip()
    valor_raw = data.get("valor")

    if not matricula or not disciplina or valor_raw is None:
        return jsonify({"erro": "Os campos 'matricula', 'disciplina' e 'valor' são obrigatórios."}), 400

    try:
        valor = float(valor_raw)
    except (TypeError, ValueError):
        return jsonify({"erro": "O campo 'valor' deve ser numérico."}), 400

    try:
        nota = LancarNota(SQLiteNotaRepository()).executar(matricula, disciplina, valor)
        return jsonify({
            "mensagem": "Nota lançada com sucesso.",
            "aluno_matricula": nota.aluno_matricula,
            "disciplina": nota.disciplina,
            "valor": nota.valor,
        }), 201
    except NotaValorInvalidoError as e:
        return jsonify({"erro": str(e)}), 422


@nota_bp.route("/desempenho/<matricula>", methods=["GET"])
def consultar_desempenho(matricula: str):
    from src.interface_adapters.repositories_impl.sqlite_aluno_repository import SQLiteAlunoRepository
    resultado = ConsultarDesempenho(SQLiteNotaRepository(), SQLiteAlunoRepository()).executar(matricula)
    return jsonify(resultado), 200
