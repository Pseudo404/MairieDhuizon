import os
import sys
import django

sys.path.append(r"c:\Users\cizea\Desktop\mairieDhuizon\MairieDhuizon")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mairieDhuizon.settings')
django.setup()

from django.test import Client

client = Client(SERVER_NAME='127.0.0.1', raise_request_exception=False)

def test_url(method, url, data=None, label=None):
    label = label or url
    try:
        if method == 'GET':
            response = client.get(url)
        else:
            response = client.post(url, data or {})
        status = response.status_code
        ok = "OK" if status < 500 else "FAIL-500"
        print(f"  [{ok}] {status} {method} {label}")
        return status
    except Exception as e:
        print(f"  [EXCEPTION] {method} {label}: {e}")
        return None

print("=== Tests GET ===")
test_url('GET', '/centre-loisirs/inscription/')
test_url('GET', '/centre-loisirs/inscription/formulaire/')
test_url('GET', '/api/calendrier-loisirs/')
test_url('GET', '/inscription-periscolaire/')

print("\n=== Tests POST centre de loisirs ===")

# Sans dates => doit rendre 200 avec message d'erreur form
test_url('POST', '/centre-loisirs/inscription/formulaire/', {
    'nom_responsable_1': 'Dupont',
    'prenom_responsable_1': 'Marie',
    'adresse_responsable_1': '10 Rue de la Paix',
    'code_postal_1': '41220',
    'ville_1': 'Dhuizon',
    'portable_1': '0602030405',
    'email_1': 'marie.dupont@email.fr',
}, label="POST sans dates")

# Avec date + 1 enfant
test_url('POST', '/centre-loisirs/inscription/formulaire/', {
    'dates': ['2026-10-10'],
    'nom_enfant_1': 'Martin',
    'prenom_enfant_1': 'Lucas',
    'date_naissance_1': '2015-06-15',
    'nom_responsable_1': 'Martin',
    'prenom_responsable_1': 'Paul',
    'adresse_responsable_1': '5 rue du Moulin',
    'code_postal_1': '41220',
    'ville_1': 'Dhuizon',
    'portable_1': '0601020304',
    'email_1': 'paul.martin@email.fr',
}, label="POST 1 enfant 1 date")

# Avec 2 dates + 2 enfants
test_url('POST', '/centre-loisirs/inscription/formulaire/', {
    'dates': ['2026-10-10', '2026-10-11'],
    'nom_enfant_1': 'Durand',
    'prenom_enfant_1': 'Emma',
    'date_naissance_1': '2017-03-20',
    'nom_enfant_2': 'Durand',
    'prenom_enfant_2': 'Leo',
    'date_naissance_2': '2019-07-10',
    'nom_responsable_1': 'Durand',
    'prenom_responsable_1': 'Claire',
    'adresse_responsable_1': '20 avenue des Pins',
    'code_postal_1': '41220',
    'ville_1': 'Dhuizon',
    'portable_1': '0701020304',
    'email_1': 'claire.durand@email.fr',
}, label="POST 2 enfants 2 dates")

print("\n=== Tests POST periscolaire ===")
test_url('POST', '/inscription-periscolaire/', {
    'nom_enfant': 'Test',
    'prenom_enfant': 'Prenom',
    'date_naissance_enfant': '2018-01-01',
    'responsable_1_nom_prenom': 'Doe John',
    'responsable_1_adresse': '1 rue Test',
    'responsable_1_telephone': '0600000000',
    'responsable_1_courriel': 'test@example.com',
    'soussigne': 'Doe John',
    'fait_a': 'Dhuizon',
    'le_date': '2026-10-01',
    'engagement_certifie': 'on',
    'engagement_cantine': 'on',
    'engagement_garderie': 'on',
}, label="POST periscolaire complet")

print("\nTermine.")
