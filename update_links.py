import re

def replace_link(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace("{% url 'actualite_detail' news_id=alerte.id %}", "{% url 'app_actualite_detail' news_id=alerte.id %}")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

replace_link('templates/app_mobile/accueil.html')
replace_link('templates/app_mobile/alertes.html')
