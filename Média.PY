# Declarando as variáveis
nota1 = float(input("Digite a nota da primeira prova: "))
nota2 = float(input("Digite a nota da segunda prova: "))

# Calculando a média
media = (nota1 + nota2) / 2

# Exibindo a média
print("A média do aluno é:", media)

# Verificando a aprovação
if media >= 6:
    print("O aluno foi aprovado!")
else:
    print("O aluno foi reprovado!")