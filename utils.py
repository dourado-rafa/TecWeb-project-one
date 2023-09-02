def extract_route(request:str) -> str:
    return '' if request == '' else request.split('\n')[0].split(' ')[1][1:]

def read_file(filepath:str) -> bytes:
    return open(filepath, 'r+b').read()

def load_template(filename:str) -> str:
    return open(f'templates/{filename}', 'r', encoding='utf-8').read()

def build_response(code:int=200, reason:str='OK', headers:str='', body:str='') -> bytes:
    headers = '\n'+headers if headers != '' else headers
    return f'HTTP/1.1 {code} {reason}{headers}\n\n{body}'.encode()