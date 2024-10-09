#Tupla de convidados
convidados = ("Alisson", "Debora", "Anderson", "André", "Gabriel", "Giselle")

#Lista de conviados
confirmados = ["Alisson", "Debora"]

#Ientificar quem ainda não confirmaram
nao_confirmados = [convidado for convidado in convidados if convidado not in confirmados]

#Exibir os convidados que ainda não confirmaram
print("Convidados que ainda não confirmaram:")
for pessoa in nao_confirmados:
    print(pessoa)

#Enviar lembretes aos não confirmados
print("\nEnviando lembretes para os convidados que ainda não confirmaram.")