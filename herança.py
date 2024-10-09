class Animal:
    def __init__(self, nome):
        self.nome = nome
    def fazer_barulho(self):
        pass
class Cachorro(Animal):
    def fazer_barulho(self):
        return "Late"
class Gato(Animal):
    def fazer_barulho(self):
        return "Mia"
    
Rex = Cachorro("Rex")
Whiskers = Gato("Whiskers")

print(f"O que o {Rex.nome} faz: {Rex.fazer_barulho()}")
print(f"O que o {Whiskers.nome} faz: {Whiskers.fazer_barulho()}")