from utils import load_data, load_template, update_data, build_response
import urllib

def index(request:str) -> str:

    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        parts = request.split('\n\n') # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        header, body = parts
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        for form_input in body.split('&'):
            key, value = urllib.parse.unquote_plus(form_input, encoding='utf-8').split('=')
            params[key] = ' '.join(value.split('+'))
        
        update_data('notes.json', params)

        return build_response(303, 'See Other', 'Location: /')

    notes_data = load_data('notes.json')

    NOTE_TEMPLATE = load_template('components/note.html')
    notes = '\n'.join([ NOTE_TEMPLATE.format(title=data['titulo'], details=data['detalhes']) for data in notes_data ])

    return build_response() + load_template('index.html').format(notes=notes).encode()
