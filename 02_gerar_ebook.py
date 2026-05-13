import os
import sys
import glob
import time
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
    print("Export a sua chave do OpenCode Go ou Z.ai no terminal: export API_KEY='sua_chave'")
    sys.exit(1)

# Inicializa o client apontando para o seu provedor
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

def ler_prompt():
    with open('prompt_consolidador.xml', 'r', encoding='utf-8') as f:
        return f.read()

def processar_chunk_com_retry(chunk_text, prompt_template, max_retries=3):
    prompt_completo = prompt_template.replace('{CHUNK_TEXT}', chunk_text)
    
    for tentativa in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "Você é um autor sênior focado em transformar dados brutos em capítulos perenes de e-book."},
                    {"role": "user", "content": prompt_completo}
                ],
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"    [Erro] Tentativa {tentativa}/{max_retries} falhou: {e}")
            if tentativa == max_retries:
                print("    [Fatal] Número máximo de tentativas atingido. Pulando chunk.")
                return ""
            time.sleep(10 * tentativa)

def processar_arquivo(arquivo_entrada, prompt_template):
    nome_refinado = arquivo_entrada.replace('.md', '_refinado.md')
    print(f"\n--- Iniciando processamento de: {arquivo_entrada} (Modelo: {MODEL_NAME}) ---")
    
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        conteudo = f.read()
        
    # DeepSeek e outros modelos aguentam chunks maiores, mantive 40k caracteres
    chunk_size = 40000
    chunks = [conteudo[i:i+chunk_size] for i in range(0, len(conteudo), chunk_size)]
    
    chunks_ja_processados = 0
    if os.path.exists(nome_refinado):
        with open(nome_refinado, 'r', encoding='utf-8') as f_out_read:
            chunks_ja_processados = f_out_read.read().count("<!-- CHUNK_END -->")
        print(f"Retomando progresso: {chunks_ja_processados}/{len(chunks)} chunks já processados.")
    else:
        with open(nome_refinado, 'w', encoding='utf-8') as f_out:
            titulo = conteudo.split('\n')[0]
            f_out.write(f"{titulo}\n\n")

    for i in range(chunks_ja_processados, len(chunks)):
        chunk = chunks[i]
        print(f"  Enviando chunk {i+1}/{len(chunks)} para a IA...")
        
        texto_refinado = processar_chunk_com_retry(chunk, prompt_template)
        
        with open(nome_refinado, 'a', encoding='utf-8') as f_out:
            if texto_refinado and "<empty/>" not in texto_refinado.lower():
                f_out.write(texto_refinado + "\n\n")
            f_out.write("<!-- CHUNK_END -->\n")
            
        time.sleep(3)
        
    print(f"--- Processamento de {arquivo_entrada} concluído! ---")

def compilar_ebook():
    arquivos_refinados = sorted(glob.glob('*_refinado.md'))
    if not arquivos_refinados:
        print("Nenhum arquivo refinado encontrado.")
        return

    print("\nCompilando Ebook_Consolidado.md...")
    with open('Ebook_Consolidado.md', 'w', encoding='utf-8') as f_final:
        f_final.write("# O Guia Definitivo: Passageiro de Primeira\n\n")
        f_final.write("## Índice\n")
        
        for arq in arquivos_refinados:
            with open(arq, 'r', encoding='utf-8') as f_ref:
                linhas = f_ref.readlines()
                if linhas:
                    titulo_original = linhas[0].strip().replace('# ', '')
                    f_final.write(f"- [{titulo_original}](#{titulo_original.lower().replace(' ', '-')})\n")
        
        f_final.write("\n---\n\n")
        
        for arq in arquivos_refinados:
            with open(arq, 'r', encoding='utf-8') as f_ref:
                conteudo_limpo = f_ref.read().replace("<!-- CHUNK_END -->\n", "")
                f_final.write(conteudo_limpo + "\n\n---\n\n")
                
    print("Ebook_Consolidado.md gerado com sucesso!")

def main():
    prompt_template = ler_prompt()
    if len(sys.argv) > 1:
        arquivo_especifico = sys.argv[1]
        if arquivo_especifico == "compilar":
            compilar_ebook()
            return
        if not os.path.exists(arquivo_especifico):
            print(f"Erro: Arquivo {arquivo_especifico} não encontrado.")
            return
        processar_arquivo(arquivo_especifico, prompt_template)
    else:
        arquivos_md = [arq for arq in sorted(glob.glob('0*.md')) if '_refinado' not in arq]
        for arquivo in arquivos_md:
            processar_arquivo(arquivo, prompt_template)
        compilar_ebook()

if __name__ == "__main__":
    main()
