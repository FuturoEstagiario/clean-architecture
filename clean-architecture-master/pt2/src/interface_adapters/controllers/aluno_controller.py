from flask import Blueprint, request, jsonify
from src.application.use_cases.cadastrar_aluno import CadastrarAluno
from src.interface_adapters.repositories_impl.sqlite_aluno_repository import SQLiteAlunoRepository

aluno_bp = Blueprint("aluno", __name__)


@aluno_bp.route("/alunos", methods=["POST"])
def cadastrar_aluno():
    data = request.get_json(silent=True) or {}
    matricula = str(data.get("matricula", "")).strip()
    nome = str(data.get("nome", "")).strip()

    if not matricula or not nome:
        return jsonify({"erro": "Os campos 'matricula' e 'nome' são obrigatórios."}), 400

    caso_de_uso = CadastrarAluno(SQLiteAlunoRepository())
    caso_de_uso.executar(matricula, nome)

    return jsonify({"mensagem": f"Aluno '{nome}' cadastrado com sucesso.", "matricula": matricula}), 201
