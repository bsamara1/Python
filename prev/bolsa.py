class Bolsa:
    def __init__(self, id, nome_bolsa, valor, media_minima, rendimento_maximo):
        self.id = id
        self.nome_bolsa = nome_bolsa
        self.valor = valor
        self.media_minima = media_minima
        self.rendimento_maximo = rendimento_maximo

    def __str__(self):
        return f"{self.nome_bolsa} - {self.valor} CVE"