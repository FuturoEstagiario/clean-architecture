class AutenticacaoDTO:
    def __init__(self, login: str, nome: str, perfil: str, autenticado: bool, token: str = ""):
        self.login = login
        self.nome = nome
        self.perfil = perfil
        self.autenticado = autenticado
        self.token = token
