from src.domain.entities.usuario import Usuario
from src.application.repositories.usuario_repository import IUsuarioRepository
from src.infrastructure.database.sqlite_connection import SQLiteConnection

class SQLiteUsuarioRepository(IUsuarioRepository):
    def __init__(self, connection_manager: SQLiteConnection):
        self.connection_manager = connection_manager

    def salvar(self, usuario: Usuario) -> None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO usuarios (login, nome, perfil, senha_hash) VALUES (?, ?, ?, ?)",
            (usuario.login, usuario.nome, usuario.perfil, usuario.senha_hash),
        )
        conn.commit()
        conn.close()

    def buscar_por_login(self, login: str) -> Usuario | None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT login, nome, perfil, senha_hash FROM usuarios WHERE login = ?",
            (login,),
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            usuario = Usuario(row["login"], row["nome"], row["perfil"])
            usuario.senha_hash = row["senha_hash"]
            return usuario
        return None
