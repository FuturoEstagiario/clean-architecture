from typing import List
from src.domain.entities.professor import Professor
from src.application.repositories.professor_repository import IProfessorRepository
from src.infrastructure.database.sqlite_connection import SQLiteConnection

class SQLiteProfessorRepository(IProfessorRepository):
    def __init__(self, connection_manager: SQLiteConnection):
        self.connection_manager = connection_manager

    def salvar(self, professor: Professor) -> None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO professores (matricula_funcional, nome, email) VALUES (?, ?, ?)",
            (professor.matricula_funcional, professor.nome, professor.email),
        )
        conn.commit()
        conn.close()

    def buscar_por_matricula(self, matricula_funcional: str) -> Professor | None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT matricula_funcional, nome, email FROM professores WHERE matricula_funcional = ?",
            (matricula_funcional,),
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return Professor(row["matricula_funcional"], row["nome"], row["email"])
        return None

    def listar_todos(self) -> List[Professor]:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT matricula_funcional, nome, email FROM professores ORDER BY nome")
        rows = cursor.fetchall()
        conn.close()
        return [Professor(r["matricula_funcional"], r["nome"], r["email"]) for r in rows]
