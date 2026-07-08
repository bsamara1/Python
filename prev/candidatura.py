class Candidatura:
    def __init__(self, id, estudante_id, bolsa_id, data_candidatura, estado):
        self.id = id
        self.estudante_id = estudante_id
        self.bolsa_id = bolsa_id
        self.data_candidatura = data_candidatura
        self.estado = estado

    def __str__(self):
        return f"Candidatura {self.id} - {self.estado}"