import os
import sys
import random
try:
    from openai import OpenAI
except ImportError:
    print("Biblioteca openai não encontrada. Instale com: pip install openai")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Dica: instale 'python-dotenv' para carregar variáveis de um arquivo .env automaticamente.")

# Configurações dinâmicas via variáveis de ambiente
API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("API_BASE_URL", "https://api.deepseek.com/v1") 
MODEL_NAME = os.environ.get("MODEL_NAME", "deepseek-v4-pro") 

if not API_KEY:
    print("Erro: A variável de ambiente API_KEY não está configurada.")
    sys.exit(1)

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

PROMPT_ANALISE = """
Você é um Cientista de Dados e Especialista em Comunidades focado em análise de texto.
Abaixo está uma amostra de mensagens extraídas de um histórico de chat de uma comunidade.

Sua tarefa é analisar essas mensagens e fornecer um plano estruturado para extrair o conhecimento de valor desse grupo.

Por favor, forneça o seguinte:
1. NICHO DA COMUNIDADE: Qual o tema principal deste grupo?
2. SUGESTÃO DE CATEGORIAS: Sugira de 4 a 6 grandes categorias/tópicos de valor que são discutidos e que dariam bons capítulos de um E-book.
3. PALAVRAS-CHAVE PARA INCLUSÃO: Para cada categoria sugerida, liste 5 a 10 palavras-chave exatas que podem ser usadas em um script de filtragem (para encontrar essas mensagens).
4. PALAVRAS-CHAVE/ASSUNTOS PARA EXCLUSÃO (RUÍDO): O que é considerado ruído neste grupo? (Ex: gírias cotidianas, promoções que expiram, anúncios).

Amostra do Chat:
{AMOSTRA}
"""

def main():
    if not os.path.exists("historico.txt"):
        print("Erro: Arquivo 'historico.txt' não encontrado na pasta.")
        return

    print("Lendo historico.txt e gerando uma amostra representativa...")
    with open("historico.txt", "r", encoding="utf-8") as f:
        linhas = f.readlines()
        
    # Pega uma amostra de 2000 linhas espalhadas para não estourar o limite de tokens rapidamente
    if len(linhas) > 2000:
        amostra = random.sample(linhas, 2000)
    else:
        amostra = linhas
        
    texto_amostra = "".join(amostra)
    
    print(f"Analisando a comunidade usando o modelo {MODEL_NAME}... Isso pode levar um minuto.")
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Você é um analista de comunidades experiente e pragmático."},
                {"role": "user", "content": PROMPT_ANALISE.replace("{AMOSTRA}", texto_amostra)}
            ],
            temperature=0.3
        )
        print("\n" + "="*60)
        print("🎯 RESULTADO DA ANÁLISE DE DIAGNÓSTICO 🎯")
        print("="*60 + "\n")
        print(response.choices[0].message.content)
        print("\n" + "="*60)
        print("💡 DICA: Use as categorias e palavras-chave acima para configurar as variáveis do script '01_extract_insights.py' e do 'prompt_consolidador.xml'.")
        
    except Exception as e:
        print(f"Erro ao analisar o histórico: {e}")

if __name__ == "__main__":
    main()
