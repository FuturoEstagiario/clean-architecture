from typing import List
from src.domain.entities.aluno import Aluno
from src.application.repositories.aluno_repository import IAlunoRepository
from src.infrastructure.database.sqlite_connection import SQLiteConnection

class SQLiteAlunoRepository(IAlunoRepository):
    def __init__(self, connection_manager: SQLiteConnection):
        self.connection_manager = connection_manager

    def salvar(self, aluno: Aluno) -> None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO alunos (matricula, nome, situacao) VALUES (?, ?, ?)",
            (aluno.matricula, aluno.nome, aluno.situacao),
        )
        conn.commit()
        conn.close()

    def buscar_por_matricula(self, matricula: str) -> Aluno | None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT matricula, nome, situacao FROM alunos WHERE matricula = ?", (matricula,))
        row = cursor.fetchone()
        conn.close()

        if row:
            aluno = Aluno(row["matricula"], row["nome"])
            aluno.situacao = row["situacao"]
            return aluno
        return None

    def listar_todos(self) -> List[Aluno]:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT matricula, nome, situacao FROM alunos ORDER BY nome")
        rows = cursor.fetchall()
        conn.close()

        alunos = []
        for row in rows:
            aluno = Aluno(row["matricula"], row["nome"])
            aluno.situacao = row["situacao"]
            alunos.append(aluno)
        return alunos

    def atualizar_situacao(self, matricula: str, nova_situacao: str) -> None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE alunos SET situacao = ? WHERE matricula = ?",
            (nova_situacao, matricula),
        )
        conn.commit()
        conn.close()
