from flask import Flask, request, jsonify
import pickle
import re
import os
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Função para limpar texto
def limpeza_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-z\sçãáéíóúêôãà]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

# Função para encontrar sintomas parecidos
def encontrar_sintomas_parecidos(sintoma_usuario):
    user_vec = modelo_completo['vectorizer'].transform([limpeza_texto(sintoma_usuario)]).toarray()
    sim = cosine_similarity(user_vec, modelo_completo['vectors'])
    return sim.flatten()

# Função para encontrar problemas e soluções
def encontrar_problemas_solucoes(sintomas_usuario):
    problemas_encontrados = {}
    porcentagens = []

    for sintoma in sintomas_usuario:
        similaridades = encontrar_sintomas_parecidos(sintoma)
        porcentagem_media = similaridades.max() * 100  # Convertendo para porcentagem
        porcentagens.append(porcentagem_media)

        if porcentagem_media >= 50:  # Se a porcentagem for maior que 50%
            sintoma_index = similaridades.argmax()  # Sintoma mais parecido
            problema = modelo_completo['data']['possivel_problema'].iloc[sintoma_index]
            solucao = modelo_completo['data']['solucao'].iloc[sintoma_index]
            if problema in problemas_encontrados:
                problemas_encontrados[problema].append(solucao)  # Adiciona solução se o problema já existe
            else:
                problemas_encontrados[problema] = [solucao]  # Cria nova entrada para o problema

    if porcentagens:
        porcentagem_media_total = sum(porcentagens) / len(porcentagens)  # Calcula a porcentagem média
        return porcentagem_media_total, problemas_encontrados
    else:
        return 0, {}

# Função para refinar a busca de problemas e soluções
def refinar_busca(sintomas_usuario):
    while True:
        porcentagem_media, problemas = encontrar_problemas_solucoes(sintomas_usuario)

        if porcentagem_media >= 90:  # 90% ou 100%
            problema_mais_comum = max(problemas.items(), key=lambda item: len(item[1]))  # Problema com mais soluções
            return {problema_mais_comum[0]: problema_mais_comum[1]}  # Retorna o problema e suas soluções

        elif 70 <= porcentagem_media < 90:  # 70% a 90%
            return problemas  # Retorna problemas agrupados

        elif 50 <= porcentagem_media < 70:  # 50% a 70%
            return {p: s for p, s in problemas.items()}  # Retorna diagnósticos individuais

        else:
            return {}

# Carregar o modelo completo do arquivo .pickle
with open('modelo_completo.pickle', 'rb') as f:
    modelo_completo = pickle.load(f)

@app.route('/diagnostico', methods=['POST'])
def diagnostico():
    sintomas_usuario = request.json.get('sintomas', [])
    
    if not sintomas_usuario:
        return jsonify({'message': 'Nenhum sintoma foi inserido.'}), 400

    problemas = refinar_busca(sintomas_usuario)
    
    if problemas:
        # Formatação do retorno para o Watson Assistant
        resposta = []
        for problema, solucoes in problemas.items():
            resposta.append({
                'problema': problema,
                'solucoes': solucoes
            })
        return jsonify({'diagnostico': resposta})
    else:
        return jsonify({'message': 'Nenhum problema ou solução encontrada.'}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
