notas = [7.5, 1.0, 6.5, 9.0, 7.0]

# Função regular para calcular a média

def calcular_media(notas):
    total = sum(notas)
    media = total / len(notas)
    return media

# Função lambda para arredondar a média para duas casas decimais

arredondar_media = lambda medida: round(media,2)

#calcular a média
media = calcular_media(notas)
media_arredondada = arredondar_media(media)

# Verificar se os estudantes foram aprovados
if media_arredondada >= 7:
    situacao = "Aprovado"
    
else:
    situacao = "Reprovado"
    
  
print(f" As notas são: {notas}")
print(f" A media é: {media_arredondada}")
print(f" A situação é: {situacao}")