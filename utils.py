import json

def extract_route(request:str) -> str:
    return request.split('\n')[0].split(' ')[1][1:]

def read_file(filepath:str) -> bytes:
    return open(filepath, 'r+b').read()

def load_data(filename:str) -> (dict | list):
    return json.loads(read_file(f'data/{filename}'))

def load_template(filename:str) -> str:
    return open(f'templates/{filename}', 'r').read()

def update_data(filename:str, new_data:dict) -> None:
    data = load_data(filename)
    data.append(new_data)
    open(f'data/{filename}', 'w').write(json.dumps(data, indent=4, ensure_ascii=False))

def build_response(code:int=200, reason:str='OK', headers:str='', body:str='') -> bytes:
    headers = '\n'+headers if headers != '' else headers
    return f'HTTP/1.1 {code} {reason}{headers}\n\n{body}'.encode()