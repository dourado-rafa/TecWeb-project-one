from utils import load_template, build_response, extract_route
from note_database import NoteDatabase, Note
import urllib

DATABASE = NoteDatabase('notes')

def index(request: str) -> str:

    if request.startswith('POST'):
        route = extract_route(request)
        request = request.replace('\r', '')  # Remove caracteres indesejados
        parts = request.split('\n\n') # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        header, body = parts
        
        if route == 'new':
            new_note = Note()
            for form_input in body.split('&'):
                key, value = urllib.parse.unquote_plus(form_input, encoding='utf-8').split('=')
                value = ' '.join(value.split('+'))
                new_note.__setattr__(key, value)
            DATABASE.add(new_note)
        
        elif route == 'delete':
            _, id = urllib.parse.unquote_plus(body, encoding='utf-8').split('=')
            DATABASE.delete(id)

        return build_response(303, 'See Other', 'Location: /')
        

    notes_data = DATABASE.get_all()

    NOTE_TEMPLATE = load_template('components/note.html')
    notes = '\n'.join([ NOTE_TEMPLATE.format(title=note.title, content=note.content, id=note.id) for note in notes_data ])

    return build_response(headers='Location: /') + load_template('index.html').format(notes=notes).encode()

def edition(request: str) -> str:

    if request.startswith('POST'):
        route = extract_route(request)
        request = request.replace('\r', '')  # Remove caracteres indesejados
        parts = request.split('\n\n') # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        header, body = parts
        
        note = Note()
        if route == 'edit-save':
            for form_input in body.split('&'):
                key, value = urllib.parse.unquote_plus(form_input, encoding='utf-8').split('=')
                value = ' '.join(value.split('+'))
                note.__setattr__(key, value)
            DATABASE.update(note)
            return build_response(303, 'See Other', 'Location: /')
        
        else:
            _, id = urllib.parse.unquote_plus(body, encoding='utf-8').split('=')
            note = DATABASE.get(id)
            return build_response() + load_template('edit.html').format(id=note.id, title=note.title, content=note.content).encode()
        
def error(request: str) -> str:
    route = extract_route(request)
    return build_response(404, 'Not Found') + load_template('error.html').format(page=route).encode()
