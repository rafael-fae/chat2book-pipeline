import os
import sys
import glob
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

# Configurações para o DeepSeek V4 Pro (OpenCode Go)
API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("API_BASE_URL", "https://opencode.ai/zen/go/v1") 
MODEL_NAME = os.environ.get("MODEL_NAME", "deepseek-v4-pro") 

if not API_KEY:
    print("Erro: A variável de ambiente API_KEY não está configurada.")
    sys.exit(1)

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

PROMPT_CONSOLIDADOR_SEMANTICO = """
Você é o Editor-Chefe e Arquiteto de Informação do maior guia de consulta sobre o tema discutido.
O texto abaixo é o resultado de uma compilação de dicas valiosas de um grupo/comunidade digital. Devido ao processo de extração, ele está fragmentado: um mesmo assunto é abordado várias vezes de forma repetitiva ao longo do texto.

Sua missão é AGLUTINAR e DESFRAGMENTAR este conteúdo.

Regras Inegociáveis:
1. AGRUPAMENTO SEMÂNTICO: Leia todo o texto, identifique as entidades/tópicos principais e crie um único e grande sub-capítulo para cada entidade, consolidando todas as informações espalhadas sobre ela.
2. ELIMINAÇÃO DE REDUNDÂNCIAS: Se três parágrafos diferentes dizem a mesma coisa, escreva isso apenas UMA VEZ.
3. PRESERVAÇÃO DE CONHECIMENTO: Jamais perca uma dica de ouro, insight de valor, técnica citada ou alerta. Apenas reorganize.
4. ESTÉTICA E EMOJIS: Use Markdown rico. Emojis nos títulos principais (H2, H3). Dicas de ouro em blocos de citação (`> 💡 **Dica de Ouro:**`).
5. RETORNE APENAS O MARKDOWN: Não adicione textos iniciais como "Aqui está a revisão".

Texto Bruto Fragmentado:
{TEXTO_BRUTO}
"""

def aglutinar_arquivo(arquivo_entrada):
    nome_saida = arquivo_entrada.replace('_refinado.md', '_final.md')
    print(f"\n--- Aglutinando semanticamente: {arquivo_entrada} ---")
    
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # O DeepSeek V4 aguenta contextos enormes. Vamos mandar o arquivo inteiro.
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Você é um organizador semântico implacável. Agrupe informações e elimine redundâncias."},
                {"role": "user", "content": PROMPT_CONSOLIDADOR_SEMANTICO.replace("{TEXTO_BRUTO}", conteudo)}
            ],
            temperature=0.1 # Temperatura baixíssima para garantir precisão e zero alucinação
        )
        texto_final = response.choices[0].message.content
        
        with open(nome_saida, 'w', encoding='utf-8') as f_out:
            f_out.write(texto_final)
        print(f"Sucesso! Arquivo {nome_saida} gerado perfeitamente.")
        
    except Exception as e:
        print(f"Erro fatal ao processar o arquivo inteiro com o modelo: {e}")
        print("Dica: Se o erro for de limite de tokens da API, pode ser necessário dividir o arquivo na metade.")

def main():
    # Permite passar o nome do arquivo via terminal
    if len(sys.argv) > 1:
        arquivo_especifico = sys.argv[1]
        
        if not os.path.exists(arquivo_especifico):
            print(f"Erro: O arquivo {arquivo_especifico} não foi encontrado.")
            return
            
        if os.path.exists(arquivo_especifico.replace('_refinado.md', '_final.md')):
            print(f"Pulando {arquivo_especifico}, arquivo _final.md já existe.")
            return
            
        aglutinar_arquivo(arquivo_especifico)
    
    # Se não passar argumento, processa todos
    else:
        arquivos_refinados = sorted(glob.glob('*_refinado.md'))
        if not arquivos_refinados:
            print("Nenhum arquivo *_refinado.md encontrado.")
            return
            
        for arquivo in arquivos_refinados:
            if os.path.exists(arquivo.replace('_refinado.md', '_final.md')):
                print(f"Pulando {arquivo}, arquivo _final.md já existe.")
                continue
            aglutinar_arquivo(arquivo)

if __name__ == "__main__":
    main()
