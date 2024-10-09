import vscodePlot.plot as plt

# Dados
x = [1, 2, 3, 4, 5]
y = [2, 4, 1, 3, 5]

# Criar um gráfico de linha
plt.plot(x, y)

# Adicionar rótulos aos eixoa
plt.xlabel('Eixo X')
plt.ylabel('Eixo Y')

# Adicionar um título ao grafico
plt.title('Exemplo de Gráfico de linha')

# Mostrar o gráfico
plt.show()

