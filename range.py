# "z" é a variavel, cria uma sequência que começa em 1, vai até 10 (11-1) e incrementa de 2 em 2
print("#Range -------------------------------------------------------------")

for z in range(1, 11, 2):
    print(z)

#Range com break
print("#Range com break ----------------------------------------------------")

for numero in range(1, 11):
    if numero %2 == 0:
        print(f"O primeiro número par encontrado é: {numero}")
        break

#Range com continue, A execução continua com o próximo número ( pula )
print("#Range com continue ----------------------------------------------------")

for numero1 in range(1, 11):
    if numero1 == 5:
        continue
print(f"A saída será {numero1}")
