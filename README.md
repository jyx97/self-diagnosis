# 🚗 Sistema de Diagnóstico Automotivo 🚘

Este projeto implementa um sistema de diagnóstico automotivo superinteligente 🤖, desenvolvido para identificar rapidamente problemas em veículos com base em sintomas descritos. Utilizando uma API RESTful construída com **Flask** e um modelo de aprendizado de máquina treinado, o sistema analisa sintomas fornecidos pelo usuário, compara-os com um banco de dados robusto e retorna possíveis problemas e soluções com uma confiança calculada. A ideia é agilizar o processo de diagnóstico, economizando tempo e reduzindo a necessidade de testes manuais demorados, tornando a manutenção de veículos mais eficiente e acessível, especialmente em situações de emergência ou para quem não tem conhecimento técnico profundo. Ele usa a técnica de **cosine similarity** para encontrar correspondências precisas entre sintomas e problemas, trazendo respostas práticas e confiáveis em segundos! 🔧

## Funcionalidades
- Recebe sintomas automotivos via uma API RESTful (endpoint `/diagnostico`) em formato JSON. 📡
- Processa os sintomas, realiza limpeza de texto e calcula a similaridade com um conjunto de dados pré-treinado. 🧹
- Retorna problemas e soluções com base em um sistema de confiança (porcentagem de similaridade). ✅
- Gera um arquivo `.csv` com combinações expandidas de sintomas, problemas e soluções. 📄
- Compatível com integração ao **Watson Assistant** para respostas formatadas. 🤝
- Exporta um modelo completo em um arquivo `.pickle` para uso posterior. 💾

## Pré-requisitos
- Python 3.6+ 🐍
- Bibliotecas Python:
  - `flask` ✨
  - `scikit-learn` 📈
  - `pandas` 🐼
  - `numpy` 🔢
  - `joblib` 🛠️
  - `pickle` 📦
- Arquivo de dados `sprintia.csv` contendo as colunas: `cluster`, `problema`, `sintoma`, `solucao`. 📊
- Arquivo `modelo_completo.pickle` gerado pelo script para uso na API. 🔄

## Instalação
1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO> 📥
   cd <NOME_DO_REPOSITORIO>
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv 🌐
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências listadas:
   ```bash
   pip install -r requirements.txt 🚀
   ```
   Ou instale manualmente:
   ```bash
   pip install flask scikit-learn pandas numpy joblib
   ```

4. Certifique-se de que o arquivo `sprintia.csv` está na mesma pasta do script principal para processamento inicial. Após executar o script, o arquivo `problemas_agrupados.csv` e `modelo_completo.pickle` serão gerados. 📂

## Estrutura do Projeto
- **sprintia.csv**: Conjunto de dados inicial com sintomas, problemas e soluções automotivas. 📋
- **problemas_agrupados.csv**: Arquivo gerado com combinações expandidas de sintomas, problemas e soluções. 📑
- **modelo_completo.pickle**: Modelo treinado contendo o vetorizador, vetores, dados e funções. 💿
- **app.py**: Script principal da API Flask. 🖥️
- **main_script.ipynb**: Script Jupyter para pré-processamento, vetorização e geração do modelo. 📓

## Como Usar
### 1. Pré-processamento e Geração do Modelo 🛠️
Execute o script Jupyter (`main_script.ipynb`) ou um script Python equivalente para:
- Carregar e limpar os dados do arquivo `sprintia.csv`. 🧼
- Gerar combinações expandidas de sintomas e soluções (ex.: "com barulho", "e vibração"). 🔀
- Vetorizar os sintomas usando `TfidfVectorizer`. 📉
- Salvar o modelo completo em `modelo_completo.pickle`. 💾

Comando para executar o script (se convertido para `.py`):
```bash
python main_script.py
```

### 2. Iniciar a API 🌐
Execute o script da API Flask:
```bash
python app.py
```
A API será iniciada em `http://0.0.0.0:5000` (ou a porta especificada na variável de ambiente `PORT`). 🚀

### 3. Fazer Requisições à API 📬
Envie uma requisição POST para o endpoint `/diagnostico` com um corpo JSON contendo uma lista de sintomas. Exemplo:
```bash
curl -X POST http://localhost:5000/diagnostico -H "Content-Type: application/json" -d '{"sintomas": ["carro puxando para um lado", "luz de bateria acesa"]}'
```

**Resposta esperada**:
- **Sucesso**: Retorna uma lista de problemas e soluções. 🎉
  ```json
  {
    "diagnostico": [
      {
        "problema": "alinhamento da direcao",
        "solucoes": ["realizar alinhamento da direcao", "trocar alinhamento da direcao"]
      },
      {
        "problema": "alternador defeituoso",
        "solucoes": ["substituir o alternador", "trocar o alternador"]
      }
    ]
  }
  ```
- **Erro (sem sintomas)**: Status 400. 🚫
  ```json
  {
    "message": "Nenhum sintoma foi inserido."
  }
  ```
- **Erro (sem correspondência)**: Status 404. 😕
  ```json
  {
    "message": "Nenhum problema ou solução encontrada."
  }
  ```

### 4. Teste Interativo (Opcional) 🖱️
O script inclui um modo interativo para entrada de sintomas via terminal:
```python
sintomas_usuario = []
while True:
    sintoma = input("Digite um sintoma (ou pressione Enter para sair): ").strip()
    if sintoma:
        sintomas_usuario.append(sintoma)
    else:
        break
```
Os resultados são exibidos no terminal com problemas e soluções formatados. 📜

## Estrutura do Código
### Pré-processamento 🧹
- **`limpeza_texto(texto)`**: Converte texto para minúsculas, remove caracteres não alfabéticos e normaliza espaços. 🧼
- **Agrupamento de dados**: Gera combinações expandidas de sintomas (com variações como "com barulho" e "e vibração") e soluções (ex.: "substituir", "trocar", "realizar a troca"). 🔄
- **Vetorização**: Usa `TfidfVectorizer` para transformar sintomas em vetores numéricos para cálculo de similaridade. 📊

### Funções Principais ⚙️
- **`encontrar_sintomas_parecidos(sintoma_usuario)`**: Calcula a similaridade de cosseno entre o sintoma do usuário e o banco de dados. 📈
- **`encontrar_problemas_solucoes(sintomas_usuario)`**: Identifica problemas e soluções com base na similaridade (limiar de 50%). 🔍
- **`refinar_busca(sintomas_usuario)`**: Refina o diagnóstico com base na porcentagem média de similaridade:
  - ≥90%: Retorna o problema mais comum. 🥇
  - 70-90%: Retorna problemas agrupados. 📚
  - 50-70%: Retorna diagnósticos individuais. 📝
  - <50%: Retorna vazio. 🚫
- **Endpoint `/diagnostico`**: Processa requisições POST, valida sintomas e retorna diagnósticos em formato JSON. 📡

### Exportação do Modelo 💾
- O modelo completo (dados, vetorizador, vetores e funções) é salvo em `modelo_completo.pickle` para uso na API. 📦

## Variáveis de Ambiente 🌍
- `PORT`: Define a porta do servidor Flask (padrão: 5000). 🔢

