import glob
import re

def gerar_ancora(texto):
    """Gera um link âncora Markdown a partir de um título."""
    texto = texto.lower()
    # Remove emojis e caracteres especiais, troca espaços por hifens
    texto = re.sub(r'[^\w\s-]', '', texto)
    texto = re.sub(r'[\s]+', '-', texto).strip('-')
    return texto

def limpar_linhas(linhas):
    """Remove blocos de código Markdown que a IA pode ter adicionado acidentalmente."""
    linhas_limpas = []
    for linha in linhas:
        linha_strip = linha.strip()
        if linha_strip == '```markdown' or linha_strip == '```':
            continue # Ignora essas linhas para não quebrar o renderizador PDF
        linhas_limpas.append(linha)
    return linhas_limpas

def main():
    arquivos_finais = sorted(glob.glob('*_final.md'))
    if not arquivos_finais:
        print("Nenhum arquivo *_final.md encontrado no diretório.")
        return

    print("Gerando o Índice com âncoras HTML nativas...")
    
    indice = ["## 📑 Índice Geral\n"]
    conteudo_total = []

    for arquivo in arquivos_finais:
        with open(arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()

        if not linhas:
            continue
            
        linhas = limpar_linhas(linhas)
            
        # Pega o primeiro H1 (#) como título do capítulo
        titulo_capitulo = ""
        for linha in linhas:
            if linha.startswith('# '):
                titulo_capitulo = linha.strip().replace('# ', '')
                break
                
        if not titulo_capitulo:
            titulo_capitulo = arquivo.replace('_final_premium.md', '').replace('_premium.md', '').replace('-', ' ').title()

        ancora_cap = gerar_ancora(titulo_capitulo)
        indice.append(f"- **[{titulo_capitulo}](#{ancora_cap})**")
        
        # Processa as linhas e INJETA o HTML das âncoras invisíveis
        linhas_processadas = []
        for linha in linhas:
            if linha.startswith('# '):
                titulo = linha.strip().replace('# ', '')
                ancora = gerar_ancora(titulo)
                # Injeta a âncora HTML imediatamente antes do título
                linhas_processadas.append(f'<a name="{ancora}" id="{ancora}"></a>\n')
                linhas_processadas.append(linha)
            elif linha.startswith('## '):
                subtitulo = linha.strip().replace('## ', '')
                ancora = gerar_ancora(subtitulo)
                indice.append(f"  - [{subtitulo}](#{ancora})")
                # Injeta a âncora HTML imediatamente antes do subtítulo
                linhas_processadas.append(f'<a name="{ancora}" id="{ancora}"></a>\n')
                linhas_processadas.append(linha)
            else:
                linhas_processadas.append(linha)

        conteudo_total.append(f"<!-- CAPITULO: {titulo_capitulo} -->\n")
        conteudo_total.extend(linhas_processadas)
        conteudo_total.append("\n---\n\n")

    with open('Ebook_Consolidado_Comunidade.md', 'w', encoding='utf-8') as f_out:
        # Capa / Título Principal
        f_out.write("# 📚 O Guia Definitivo da Comunidade\n")
        f_out.write("> *Compilação Oficial de Dicas, Hacks e Regras Perenes extraídas do Chat*\n\n---\n\n")
        
        # Escreve o Índice
        f_out.write("\n".join(indice))
        f_out.write("\n\n---\n\n")
        
        # Escreve o conteúdo com as âncoras
        f_out.writelines(conteudo_total)

    print("\n✅ Compilação concluída com sucesso!")
    print("O arquivo 'Ebook_Consolidado_Comunidade.md' foi gerado sem tags de código residuais e com âncoras HTML inseridas.")

if __name__ == "__main__":
    main()
