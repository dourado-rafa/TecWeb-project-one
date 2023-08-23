from utils import load_template, build_response
from note_database import NoteDatabase, Note
import urllib

DATABASE = NoteDatabase('notes')

def index(request:str) -> str:

    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        parts = request.split('\n\n') # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        header, body = parts

        new_note = Note()
        for form_input in body.split('&'):
            key, value = urllib.parse.unquote_plus(form_input, encoding='utf-8').split('=')
            value = ' '.join(value.split('+'))
            new_note.__setattr__(key, value)
        DATABASE.add(new_note)

        return build_response(303, 'See Other', 'Location: /')

    notes_data = DATABASE.get_all()

    NOTE_TEMPLATE = load_template('components/note.html')
    notes = '\n'.join([ NOTE_TEMPLATE.format(title=note.title, content=note.content) for note in notes_data ])

    return build_response() + load_template('index.html').format(notes=notes).encode()
