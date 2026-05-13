# 🚀 Chat2Book Pipeline: De Histórico de Chat a E-book Profissional

O **Chat2Book Pipeline** é uma solução completa para transformar arquivos brutos de exportação de chat (como WhatsApp ou Telegram) em um E-book consolidado, perene e com formatação premium.

O projeto utiliza **Python** para processamento de arquivos e **Inteligência Artificial (LLMs de longo contexto como DeepSeek e Gemini)** para limpeza semântica, remoção de ruídos temporais e organização editorial.

---

## ⚙️ Setup Inicial

### 1. Requisitos
Certifique-se de ter o Python instalado. Instale as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

### 2. Configuração de Ambiente
Crie um arquivo `.env` na raiz do projeto com suas chaves de API. O pipeline suporta provedores compatíveis com a biblioteca da OpenAI (OpenRouter, DeepSeek, OpenCode Go, etc):

```env
API_KEY="sua_chave_api_aqui"
API_BASE_URL="https://opencode.ai/zen/go/v1"
MODEL_NAME="deepseek-v4-pro"
```

### 3. Dados de Entrada (Exportando o Histórico)
Para o pipeline funcionar, você precisa fornecer o arquivo bruto do chat com o nome **`historico.txt`** na raiz do projeto.

**Como exportar do WhatsApp:**
1. Abra o grupo ou conversa no WhatsApp (pelo celular).
2. Toque no nome do grupo (no topo).
3. Role até o final e selecione **"Exportar conversa"**.
4. Escolha a opção **"Sem mídia"** (isso gera um arquivo `.txt` apenas com os textos).
5. Salve o arquivo gerado, renomeie-o para `historico.txt` e coloque-o na pasta principal do seu projeto.

---

## 🛠️ O Fluxo de Execução (Pipeline 00 a 06)

O pipeline foi projetado para ser executado de forma estritamente sequencial, do passo `00` ao `06`. Cada script realiza uma transformação específica nos dados, passando o resultado para a próxima etapa.

### `00` - Diagnóstico da Comunidade
Analisa uma pequena amostra do `historico.txt` usando IA para descobrir o nicho do grupo, sugerir as grandes categorias para o E-book e recomendar palavras-chave.
- **Como usar:** `python 00_analisar_historico.py`
- **Ação:** Com o resultado deste script, você deve abrir o arquivo `02_categorizar_mensagens.py` e editar o dicionário `categories` com as palavras-chave sugeridas.

### `01` - Filtragem por Sessões Temporais
Lê o `historico.txt` bruto e agrupa as mensagens baseando-se em proximidade de tempo (sessões de 15 minutos). O script ignora conversas irrelevantes e mantém apenas blocos onde certas palavras-chave (definidas no código) aparecem múltiplas vezes.
- **Como usar:** `python 01_filtrar_sessoes.py`
- **Saída:** Gera o arquivo `filtered_historico.txt` contendo apenas as conversas com potencial.

### `02` - Categorização e Limpeza Bruta
Lê o `filtered_historico.txt`, remove metadados do WhatsApp (datas, horas, nomes de usuários) e usa heurísticas de palavras-chave para distribuir as mensagens nos tópicos (capítulos) adequados.
- **Como usar:** `python 02_categorizar_mensagens.py`
- **Saída:** Gera múltiplos arquivos `.md` (ex: `01-acumulo.md`, `02-emissoes.md`).

### `03` - Refinamento de Conteúdo Perene (Chunking)
Processa cada arquivo Markdown em blocos (chunks) usando a IA. O objetivo aqui é **remover ruído temporal**: promoções expiradas, preços antigos ou discussões irrelevantes, mantendo apenas regras duradouras.
- **Como usar:** `python 03_refinar_ia_chunking.py`
- **Saída:** Gera arquivos com o sufixo `_refinado.md`.

### `04` - Aglutinação Semântica (Map-Reduce)
Devido ao processamento em blocos do passo anterior, informações sobre a mesma coisa (ex: "Livelo") podem ficar espalhadas. Este passo joga o arquivo inteiro em uma IA de contexto massivo para desfragmentar o conteúdo, aglutinando tudo o que for semelhante em um único bloco contínuo e eliminando repetições.
- **Como usar:** `python 04_aglutinar_semantica.py`
- **Saída:** Gera arquivos com o sufixo `_final.md`.

### `05` - Formatação e Polimento Premium
Aplica a identidade visual do seu E-book. A IA revisa o texto inserindo emojis elegantes nos títulos (H1, H2, H3), transforma dicas importantes em blocos de citação Markdown (`> 💡 Dica de Ouro`) e converte dados estruturados em tabelas para melhorar a leitura.
- **Como usar:** `python 05_formatar_premium.py`
- **Saída:** Gera arquivos com o sufixo `_premium.md`.

### `06` - Compilação Final e Geração de Índice
Junta todos os arquivos `_premium.md` em um único arquivo mestre. Adiciona um sumário (índice) no topo com âncoras HTML nativas invisíveis, permitindo que os links funcionem perfeitamente quando convertido para PDF.
- **Como usar:** `python 06_compilar_ebook.py`
- **Saída:** Gera o arquivo final `Ebook_Consolidado_Comunidade.md`.

---

## 🖨️ Conversão para PDF

Com o seu arquivo `.md` consolidado em mãos, utilize o `mdpdf` para gerar o e-book final:

```bash
npx mdpdf Ebook_Consolidado_Comunidade.md
```

---
*Desenvolvido para transformar conversas em conhecimento estruturado.*
