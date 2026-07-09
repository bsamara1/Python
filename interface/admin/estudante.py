class Estudante:
    def __init__(self, id, nome, email, universidade, curso, media, rendimento_familiar):
        self.id = id
        self.nome = nome
        self.email = email
        self.universidade = universidade
        self.curso = curso
        self.media = media
        self.rendimento_familiar = rendimento_familiar

    def __str__(self):
        return f"{self.nome} - {self.universidade} - {self.curso}"