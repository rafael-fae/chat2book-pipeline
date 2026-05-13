import os
import sys
try:
    from openai import OpenAI
except ImportError:
    print("Biblioteca openai não encontrada. Instale com: pip install openai")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configurações dinâmicas via variáveis de ambiente
API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("API_BASE_URL", "https://opencode.ai/zen/go/v1") 
MODEL_NAME = os.environ.get("MODEL_NAME", "deepseek-v4-pro") 

if not API_KEY:
    print("Erro: A variável de ambiente API_KEY não está configurada.")
    sys.exit(1)

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

PROMPT_REVISOR = """
Você é um Designer Editorial e Especialista em Milhas.
Seu objetivo é pegar um rascunho de um capítulo de E-book (escrito em Markdown simples) e aplicar um polimento premium para unificar a identidade visual do livro.

Regras Inegociáveis:
1. NÃO remova NENHUMA informação técnica, dica, regra ou valor. O conteúdo já foi validado, você é apenas o diagramador.
2. Adicione emojis pertinentes e elegantes em TODOS os títulos (H1, H2, H3). Ex: "## 💳 Limites de Cartões".
3. Encontre as dicas mais valiosas e macetes espalhados pelo texto e coloque-os em blocos de citação Markdown (`> 💡 **Dica de Ouro:** ...`).
4. Garanta espaçamento limpo e parágrafos curtos.
5. Se identificar informações confusas que possam virar uma tabela, converta-as para tabela Markdown.
6. Não adicione saudações ("Aqui está o texto revisado..."). Retorne apenas o Markdown.
"""

def revisar_capitulo(arquivo_entrada):
    print(f"\nAplicando polimento final em: {arquivo_entrada}")
    
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Diferente do script anterior, podemos tentar mandar o capítulo inteiro se não for gigantesco.
    # Mas como precaução, se for maior que 60k chars, dividimos.
    chunk_size = 60000
    chunks = [conteudo[i:i+chunk_size] for i in range(0, len(conteudo), chunk_size)]
    
    texto_final = ""
    for i, chunk in enumerate(chunks):
        print(f"  Polindo parte {i+1}/{len(chunks)}...")
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": PROMPT_REVISOR},
                    {"role": "user", "content": f"Aplique a identidade visual Premium no seguinte texto:\n\n{chunk}"}
                ],
                temperature=0.3
            )
            texto_final += response.choices[0].message.content + "\n\n"
        except Exception as e:
            print(f"  [Erro] Falha ao revisar parte: {e}")
            texto_final += chunk # Se falhar, mantém o original
            
    with open(arquivo_entrada.replace('.md', '_premium.md'), 'w', encoding='utf-8') as f:
        f.write(texto_final)
    print("Concluído!")

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 formatador_final.py nome_do_arquivo.md")
        return
        
    arquivo = sys.argv[1]
    if os.path.exists(arquivo):
        revisar_capitulo(arquivo)
    else:
        print(f"Arquivo não encontrado: {arquivo}")

if __name__ == "__main__":
    main()
