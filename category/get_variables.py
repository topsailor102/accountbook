import os, json

def get_variables_list():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    secret_file = os.path.join(BASE_DIR, 'secrets.json')
    with open(secret_file) as f:
        secrets = json.loads(f.read())
    
    return secrets
