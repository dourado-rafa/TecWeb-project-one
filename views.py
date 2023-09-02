from utils import load_template, build_response, extract_route
from note_database import NoteDatabase, Note
import urllib

DATABASE = NoteDatabase('notes')

def index():
    notes_data = DATABASE.get_all()
    NOTE_TEMPLATE = load_template('components/note.html')
    notes = '\n'.join([ NOTE_TEMPLATE.format(title=note.title, content=note.content, id=note.id) for note in notes_data ])
    return build_response() + load_template('index.html').format(notes=notes).encode()

def delete_note(request):
    route = extract_route(request)
    id = route.split('/')[-1]

    if id.isnumeric():
        DATABASE.delete(int(id))
        return build_response()
    return error(request, 405, 'Method Not Allowed')

def create_note(request):
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        header, body = request.split('\n\n') # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        
        new_note = Note()
        for form_input in body.split('&'):
            key, value = urllib.parse.unquote_plus(form_input, encoding='utf-8').split('=')
            value = ' '.join(value.split('+'))
            new_note.__setattr__(key, value)

        new_note.id = DATABASE.add(new_note)
        return build_response() + load_template('components/note.html').format(id=new_note.id, title=new_note.title, content=new_note.content).encode()
    return error(request, 401, 'Unauthorized')

def edit_note(request):
    route = extract_route(request)
    id = route.split('/')[-1]

    if id.isnumeric():
        note = DATABASE.get(int(id))
        return build_response() + load_template('edit.html').format(id=note.id, title=note.title, content=note.content).encode()
    return error(request)

def update_note(request):
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        header, body = request.split('\n\n') # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        
        note = Note()
        for form_input in body.split('&'):
            key, value = urllib.parse.unquote_plus(form_input, encoding='utf-8').split('=')
            value = ' '.join(value.split('+'))
            note.__setattr__(key, value)

        DATABASE.update(note)
        return build_response(303, 'See Other', 'Location: /')
    return error(request, 401, 'Unauthorized')
        
def error(request, code=404, reason='Not Found'):
    route = extract_route(request)
    return build_response(code, reason) + load_template('error.html').format(code=code, reason=reason, page=route).encode()
