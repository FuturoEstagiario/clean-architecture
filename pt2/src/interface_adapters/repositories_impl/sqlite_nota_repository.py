from src.domain.entities.nota import Nota
from src.application.repositories.nota_repository import INotaRepository
from src.infrastructure.database.sqlite_connection import SQLiteConnection

class SQLiteNotaRepository(INotaRepository):
    def __init__(self, connection_manager: SQLiteConnection):
        self.connection_manager = connection_manager

    def salvar(self, nota: Nota) -> None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notas (aluno_matricula, disciplina_codigo, valor, tipo_avaliacao) VALUES (?, ?, ?, ?)",
            (nota.aluno_matricula, nota.disciplina_codigo, nota.valor, nota.tipo_avaliacao)
        )
        conn.commit()
        conn.close()

    def buscar_por_aluno(self, aluno_matricula: str) -> list[Nota]:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT aluno_matricula, disciplina_codigo, valor, tipo_avaliacao FROM notas WHERE aluno_matricula = ?",
            (aluno_matricula,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [Nota(r["aluno_matricula"], r["disciplina_codigo"], r["valor"], r["tipo_avaliacao"]) for r in rows]

    def buscar_por_aluno_e_disciplina(self, aluno_matricula: str, disciplina_codigo: str) -> list[Nota]:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT aluno_matricula, disciplina_codigo, valor, tipo_avaliacao FROM notas WHERE aluno_matricula = ? AND disciplina_codigo = ?",
            (aluno_matricula, disciplina_codigo)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [Nota(r["aluno_matricula"], r["disciplina_codigo"], r["valor"], r["tipo_avaliacao"]) for r in rows]
