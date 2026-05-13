import re
from datetime import datetime

KEYWORDS = [
    'latam', 'smiles', 'azul', 'gol', 'tap ', 'iberia', 'qatar', 'emirates', 'american airlines', 'aadvantage',
    'delta', 'united', 'air france', 'klm', 'flying blue', 'virgin', 'british', 'executive club',
    'esfera', 'livelo', 'c6', 'itau', 'itaú', 'bradesco', 'santander', 'porto seguro', 'banco do brasil', 'brb',
    'dux', 'unlimited', 'the one', 'centurion', 'amex', 'platinum', 'black', 'infinite',
    'sala vip', 'loungekey', 'priority pass', 'dragonpass', 'wpremium', 'advantage', 'ambar', 'plaza premium',
    'all accor', 'marriott', 'hilton', 'hyatt', 'ibis', 'novotel',
    'milha', 'avios', 'ponto', 'executiva', 'business', 'first class', 'primeira classe', 'tarifa', 'tabela fixa',
    'sweet spot', 'emissão', 'emissao', 'stopover', 'status', 'diamante', 'black signature', 'emerald'
]

pattern = re.compile(r'\[(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}:\d{2})\] (.*)')

def parse_time(date_str, time_str):
    try:
        return datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M:%S")
    except Exception:
        return None

def main():
    messages = []
    current_msg = ""
    current_time = None
    
    with open('historico.txt', 'r', encoding='utf-8') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                if current_msg:
                    messages.append({'time': current_time, 'text': current_msg})
                date_str, time_str, content = match.groups()
                current_time = parse_time(date_str, time_str)
                current_msg = line
            else:
                current_msg += line
        if current_msg:
            messages.append({'time': current_time, 'text': current_msg})

    # Group into sessions (e.g. 15 minutes gap)
    sessions = []
    current_session = []
    
    for msg in messages:
        if not current_session:
            current_session.append(msg)
        else:
            last_time = current_session[-1]['time']
            curr_time = msg['time']
            if last_time and curr_time and (curr_time - last_time).total_seconds() > 15 * 60:
                sessions.append(current_session)
                current_session = [msg]
            else:
                current_session.append(msg)
    
    if current_session:
        sessions.append(current_session)

    # Filter sessions
    filtered_sessions = []
    keyword_regex = re.compile(r'(?i)\b(?:' + '|'.join(KEYWORDS) + r')\b')
    
    for session in sessions:
        session_text = "".join([m['text'] for m in session])
        # Find if session has rich content
        if keyword_regex.search(session_text):
            # Also ensure it has some substantial discussion, not just a passing mention
            matches = len(keyword_regex.findall(session_text))
            if matches >= 2: # At least 2 keyword mentions in the session
                filtered_sessions.append(session)

    with open('filtered_historico.txt', 'w', encoding='utf-8') as f:
        for session in filtered_sessions:
            for msg in session:
                f.write(msg['text'])
            f.write("-" * 50 + "\n")

    print(f"Total original messages: {len(messages)}")
    print(f"Total original sessions: {len(sessions)}")
    print(f"Total filtered sessions: {len(filtered_sessions)}")
    
if __name__ == "__main__":
    main()
