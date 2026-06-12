import hashlib

class Usuario:
    PERFIS_VALIDOS = {"aluno", "professor", "administrador"}

    def __init__(self, login: str, nome: str, perfil: str):
        if perfil not in self.PERFIS_VALIDOS:
            validos = ", ".join(sorted(self.PERFIS_VALIDOS))
            raise ValueError(f"Perfil inválido. Permitidos: {validos}.")
        if not login:
            raise ValueError("O login é obrigatório.")
        self.login = login
        self.nome = nome
        self.perfil = perfil
        self._senha_hash: str = ""

    def definir_senha(self, senha: str) -> None:
        if len(senha) < 4:
            raise ValueError("A senha deve ter pelo menos 4 caracteres.")
        self._senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    def verificar_senha(self, senha: str) -> bool:
        return self._senha_hash == hashlib.sha256(senha.encode()).hexdigest()

    @property
    def senha_hash(self) -> str:
        return self._senha_hash

    @senha_hash.setter
    def senha_hash(self, value: str) -> None:
        self._senha_hash = value
