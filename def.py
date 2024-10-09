#Definindo uma função chamada "div"

def div(a,b):
    resultado = a * b
    return resultado

# Chamando a função e armazenando o resultado em uma variável

resultado_div = div(5, 8)

# Imprimindo o resultado

print(f" O resultado da multiplicação de 5 e 8 é: {resultado_div}")

#####################################################################

#Definindo uma função chamada "soma"

def soma(c,d):
    resultado = c + d
    return resultado

# Chamando a função e armazenando o resultado em uma variável

resultado_soma = soma(5, 5)

# Imprimindo o resultado

print(f" O resultado da soma de 5 e 5 é: {resultado_soma}")

#####################################################################

#Definindo uma função chamada "e_par"

def e_par(numero):
    if numero % 2 == 0:
        return True
    else:
        return False
    
# Testando a função e_par

numero = 7
if e_par(numero):
    print(f'{numero} é um numero par')

else:
    print(f'{numero} não é um numero par')