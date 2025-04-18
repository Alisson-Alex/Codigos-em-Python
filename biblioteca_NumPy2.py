# Importe as bibliotecas necessárias
import numpy as np

# Dados dos participantes
participantes = [
    {
        "nome": "Alisson",
        "localizacao": "Araquari",
        "afiliacao": "Anhanguera",
        "interesses": ["DevOps", "CloudOps"]

    },
    {
        "nome": "Debora",
        "localizacao": "Araquari",
        "afiliacao": "SIGGA",
        "interesses": ["Enfermagem", "Instrumentadora"]
    },
    {
        "nome": "Gabriel",
        "localizacao": "Joinville",
        "afiliacao": "Anhanguera",
        "interesses": ["Engenheiro de software", "Design"]
    }
    #Adicione mais participantes conforme necessário
]

# Usando sets para identificar diferentes regiões dos participantes
regioes = set(participante["localizacao"]for participante in participantes)

# Usando um dicionário para categorizar afiliações
afiliacoes = {}

for participante in participantes:
    afiliacao = participante["afiliacao"]
    if afiliacao not in afiliacoes:
        afiliacoes[afiliacao]=[]
    afiliacoes[afiliacao].append(participante["nome"])

# Usando NumPy para parar analisar áreas de interesse
areas_de_interesse = np.array([interesse for participante in participantes for interesse in participante["interesses"]])

interesses_unicos, contagem = np.unique(areas_de_interesse, return_counts=True)

area_mais_popular = interesses_unicos[np.argmax(contagem)]