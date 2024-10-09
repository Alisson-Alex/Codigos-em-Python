precos_em_dolares = [100, 300, 50, 800, 1299, 19]
cambio = 5.25



precos_em_reais = list(map(lambda x: x * cambio, precos_em_dolares))
print(f"\nO preço dos itens em dolares eram: {precos_em_dolares}\n")
print(f"E convertidos em Reais ficaram por: {precos_em_reais}\n")