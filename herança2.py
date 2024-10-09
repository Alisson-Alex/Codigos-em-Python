class Pessoa:
    def __init__(self, nome):
        self.nome = nome
    def fazer_barulho(self):
        pass

class Animal:
    def __init__(self,nome1):
        self.nome1 = nome1
    def fazer_barulho(self):
        pass

class Humano_F(Pessoa):
    def fazer_barulho(self):
        return "Fala muito"
    
class Humano_M1(Pessoa):
    def fazer_barulho(self):
        return "Fala baixo nengue"
    
class Humano_M2(Pessoa):
    def fazer_barulho(self):
        return "Se esconde"
    
class Lagarto(Animal):
    def fazer_barulho(self):
        return "Corre"

Thaynara = Humano_F("Thaynara")  
Cuanamata = Humano_M1("Cuanamata") 
Gabriel = Humano_M2("Gabriel")
Charnmander = Lagarto("Charmander")

print(f"O que a {Thaynara.nome} faz: {Thaynara.fazer_barulho()}")
print(f"O que o {Cuanamata.nome} faz: {Cuanamata.fazer_barulho()}")
print(f"O que o {Gabriel.nome} faz: {Gabriel.fazer_barulho()}")
print(f"O que o {Charnmander.nome1} faz: {Charnmander.fazer_barulho()}")