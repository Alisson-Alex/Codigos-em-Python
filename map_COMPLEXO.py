preco_dolar = [100, 300, 50]
cambio = 5.25
taxadd = 80
porcent = 100
preco_reais = list(map(lambda x: x * cambio, preco_dolar))
taxa = list(map(lambda y: y * taxadd, preco_reais))
taxa = list(map(lambda r: r / porcent, taxa))
valor_final = list(map(lambda v1, v2: v1 + v2, taxa, preco_reais))



print(f"\nO preço dos itens em dolares eram: {preco_dolar}\n")
print(f"Preço em reais: {preco_reais}\n")
print(f"Taxa de importação é: {taxa}\n")
print(f"Agora faz o L: {valor_final}\n")