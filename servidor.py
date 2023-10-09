import socket
from pathlib import Path
from utils import extract_route, read_file, build_response
from views import index, only_notes, create_note, delete_note, edit_note, update_note, error

CUR_DIR = Path(__file__).parent
SERVER_HOST = 'localhost'
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()
    request_text = request.split('\n')
    print('===== Nova Requisição =====' + '\n' + request_text[0] + '\n' + request_text[-1] + '\n')

    route = extract_route(request)
    filepath = CUR_DIR / route
    
    if filepath.is_file():
        response = build_response() + read_file(filepath)

    elif route == '':
        response = index()
    
    elif route == 'notes':
        response = only_notes()

    elif 'create' in route:
        response = create_note(request)

    elif 'delete' in route:
        response = delete_note(request)

    elif 'edit' in route:
        response = edit_note(request)
    
    elif 'update' in route:
        response = update_note(request)

    else:
        response = error(request)

    client_connection.sendall(response)
    client_connection.close()

server_socket.close()