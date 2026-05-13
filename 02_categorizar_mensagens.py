import re
import os

def categorize_message(text):
    text_lower = text.lower()
    
    categories = {
        '01-acumulo-e-promocoes': ['acumulo', 'acúmulo', 'promocao', 'promoção', 'bônus', 'bonus', 'transferência', 'transferencia', 'bateu ganhou', 'esfera', 'livelo'],
        '02-emissoes-e-sweet-spots': ['emissão', 'emissao', 'emitir', 'sweet spot', 'tabela fixa', 'executiva', 'business', 'first class', 'aadvantage', 'latam pass', 'miles&go', 'iberia plus', 'avios', 'qsuites'],
        '03-cartoes-de-credito': ['cartão', 'cartao', 'anuidade', 'limite', 'isenção', 'isencao', 'dux', 'unlimited', 'the one', 'centurion', 'visa infinite', 'mastercard black', 'amex platinum', 'aadvantage black'],
        '04-salas-vip-e-beneficios': ['sala vip', 'lounge', 'priority pass', 'loungekey', 'wpremium', 'dragonpass', 'advantage', 'bradesco nova'],
        '05-hoteis-e-viagens': ['hotel', 'hoteis', 'hotéis', 'pousada', 'resort', 'all accor', 'marriott', 'hilton', 'hyatt', 'seguro viagem', 'locação', 'aluguel de carro'],
    }
    
    matched = []
    for cat, kws in categories.items():
        if any(kw in text_lower for kw in kws):
            matched.append(cat)
            
    if not matched:
        if any(kw in text_lower for kw in ['dica', 'vale a pena', 'recomendo', 'macete', 'desconto']):
            return ['06-insights-gerais']
        return []
    
    return matched

def clean_message(text):
    # Remove timestamps and phone numbers
    text = re.sub(r'\[\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2}\]', '', text)
    text = re.sub(r'\+55\s\d{2}\s\d{4,5}-\d{4}', '[Usuário]', text)
    text = re.sub(r'~?[^\:]+:\s', '', text, count=1)
    text = re.sub(r'‎imagem ocultada|‎vídeo omitido|‎figurinha omitida|‎Mensagem apagada|‎<Mensagem editada>', '', text)
    return text.strip()

def main():
    messages = []
    current_msg = ""
    
    # Read the file
    pattern = re.compile(r'\[\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2}\]')
    input_file = 'filtered_historico.txt' if os.path.exists('filtered_historico.txt') else 'historico.txt'
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if pattern.match(line):
                if current_msg:
                    messages.append(current_msg)
                current_msg = line
            else:
                current_msg += line
        if current_msg:
            messages.append(current_msg)

    # Process and categorize
    results = {
        '01-acumulo-e-promocoes': set(),
        '02-emissoes-e-sweet-spots': set(),
        '03-cartoes-de-credito': set(),
        '04-salas-vip-e-beneficios': set(),
        '05-hoteis-e-viagens': set(),
        '06-insights-gerais': set()
    }
    
    # Heuristics: a good tip usually has more than 50 chars, or mentions specific values/numbers
    for msg in messages:
        clean_msg = clean_message(msg)
        if len(clean_msg) < 40:
            continue
            
        cats = categorize_message(clean_msg)
        if cats:
            # We want to keep it action-oriented if possible, but for now we just collect the raw tips
            for cat in cats:
                # Add to set to remove exact duplicates
                results[cat].add(clean_msg)

    # Write to files
    titles = {
        '01-acumulo-e-promocoes': '# Estratégias de Acúmulo e Promoções\n\n',
        '02-emissoes-e-sweet-spots': '# Dicas de Emissões e Sweet Spots\n\n',
        '03-cartoes-de-credito': '# Cartões de Crédito e Benefícios\n\n',
        '04-salas-vip-e-beneficios': '# Salas VIP e Acessos\n\n',
        '05-hoteis-e-viagens': '# Hotéis, Hospedagem e Viagens\n\n',
        '06-insights-gerais': '# Insights Gerais e Outras Dicas\n\n'
    }
    
    for filename, items in results.items():
        if not items: continue
        with open(f'{filename}.md', 'w', encoding='utf-8') as f:
            f.write(titles[filename])
            for item in items:
                # Basic formatting
                f.write(f"- {item}\n\n")
                
    print("Files generated successfully.")

if __name__ == "__main__":
    main()
