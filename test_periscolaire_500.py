import os
import sys
import django

sys.path.append(r"c:\Users\cizea\Desktop\mairieDhuizon\MairieDhuizon")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mairieDhuizon.settings')
django.setup()

from django.test import Client

client = Client(SERVER_NAME='127.0.0.1')
try:
    response = client.get('/inscription-periscolaire/')
    print(f"GET Status code: {response.status_code}")
    if response.status_code == 500:
        print("Got 500 on GET.")
        
    response = client.post('/inscription-periscolaire/', {
        'nom_enfant': 'Test',
        'prenom_enfant': 'Test',
        'date_naissance_enfant': '2015-01-01',
        'responsable_1_nom_prenom': 'Doe John',
        'responsable_1_adresse': '123 Test St',
        'responsable_1_telephone': '0600000000',
        'responsable_1_courriel': 'test@example.com',
        'soussigne': 'Doe John',
        'fait_a': 'Paris',
        'le_date': '2026-10-10',
        'engagement_certifie': 'on',
        'engagement_cantine': 'on',
        'engagement_garderie': 'on'
    })
    print(f"POST Status code: {response.status_code}")
    if response.status_code == 500:
        print("Got 500 on POST.")
except Exception as e:
    import traceback
    traceback.print_exc()

