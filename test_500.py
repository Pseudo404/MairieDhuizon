import os
import sys
import django

sys.path.append(r"c:\Users\cizea\Desktop\mairieDhuizon\MairieDhuizon")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mairieDhuizon.settings')
django.setup()

from django.test import Client

client = Client(SERVER_NAME='127.0.0.1')
try:
    response = client.post('/centre-loisirs/inscription/formulaire/', {
        'dates': ['2026-10-10'],
        'nom_enfant_1': 'Test',
        'prenom_enfant_1': 'Test',
        'date_naissance_1': '2015-01-01',
        'nom_responsable_1': 'Doe',
        'prenom_responsable_1': 'John',
        'adresse_responsable_1': '123 Test St',
        'code_postal_1': '75000',
        'ville_1': 'Paris',
        'portable_1': '0600000000',
        'email_1': 'test@example.com'
    })
    print(f"Status code: {response.status_code}")
    if response.status_code == 500:
        print("Got 500.")
except Exception as e:
    import traceback
    traceback.print_exc()

