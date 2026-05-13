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
Crie um arquivo `.env` na raiz do projeto com suas chaves de API. O pipeline suporta provedores compatíveis com a biblioteca da OpenAI (OpenRouter, DeepSeek, etc):

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

## 🛠️ Arquitetura do Pipeline

O pipeline é executado em fases sequenciais para garantir a máxima qualidade e evitar perda de contexto:

### Fase 0: Diagnóstico da Comunidade
Analisa uma amostra do chat para identificar o nicho, sugerir categorias e palavras-chave de filtragem.
- **Execução:** `python 00_analisar_historico.py`

### Fase 1: Pré-Filtro e Categorização Local
Realiza uma limpeza bruta via Python, removendo metadados (timestamps, números) e separando as mensagens em arquivos Markdown por categoria. Há também um script extra para agrupar conversas por sessões temporais.
- **Execução Opcional (Sessões temporais):** `python 01_b_filter_history.py`
- **Dica:** Edite as categorias e palavras-chave dentro do script `01_extract_insights.py` com base no resultado da Fase 0.
- **Execução:** `python 01_extract_insights.py`

### Fase 2: Refinamento com IA (Chunking)
Usa a IA para processar os arquivos em blocos, removendo informações datadas (promoções expiradas, bugs antigos) e focando em conteúdo perene.
- **Configuração:** O comportamento da IA é definido pelo arquivo `prompt_consolidador.xml`.
- **Execução:** `python 02_gerar_ebook.py`

### Fase 3: Aglutinação Semântica e Polimento
Utiliza modelos de contexto massivo para desfragmentar o conteúdo. Assuntos repetidos são unidos em sub-capítulos coesos. Após a aglutinação, um script extra opcional aplica formatação premium (emojis, tabelas, blockquotes) para unificar a identidade visual.
- **Execução (Aglutinação):** `python 03_aglutinador_semantico.py`
- **Execução Opcional (Polimento):** `python 03_b_formatador_final.py nome_do_arquivo_final.md`

### Fase 4: Compilação Final e Índice
Junta todos os capítulos finalizados, gera um índice automático com âncoras HTML clicáveis e limpa resíduos de formatação.
- **Execução:** `python 04_compilar_final.py`
- **Resultado:** Gera o arquivo `Ebook_Consolidado_Comunidade.md`.

---

## 🖨️ Conversão para PDF

Para gerar o arquivo PDF final com estilo profissional, utilize o `mdpdf`:

```bash
npx mdpdf Ebook_Consolidado_Comunidade.md
```

---

## 📁 Estrutura de Arquivos

- `0*.py`: Scripts numerados de acordo com a fase de execução.
- `prompt_consolidador.xml`: Instruções detalhadas para a IA.
- `requirements.txt`: Dependências do projeto.
- `historico.txt`: Seu arquivo bruto (não incluso no repositório).
- `README.md`: Este guia de uso.

---
*Desenvolvido para transformar conversas em conhecimento estruturado.*
