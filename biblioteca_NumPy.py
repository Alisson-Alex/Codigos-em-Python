# Importe a biblioteca NumPy # Escrever o >comando< "pip install numpy"
import numpy as np

#Crie um array(variedade) Numpy de números inteiros
my_array = np.array([10, 2, 44, 20, 12])

#Imprima o array
print("Array original:")
print(my_array)

#Realize operações matematicas com o array
square_array = my_array ** 2 #Eleva cada elemento ao quadrado
sum_of_elements = np.sum(my_array) #Calcula a soma de todos os elementos

#Imprima os resultados
print("\nArray ao quadrado:")
print(square_array)
print("\nSoma dos elementos:")
print(sum_of_elements)

#Acesse elementos do array
elements_at_indez_2 = my_array[2] #Acessa o elemento no indice 2
print("\nElemento no indice 2:", elements_at_indez_2)