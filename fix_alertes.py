import re

with open('templates/app_mobile/alertes.html', 'r', encoding='utf-8') as f:
    content = f.read()

img_pattern = r'            {% if alerte\.image %}\n            <div class="mt-3 rounded-xl overflow-hidden relative mb-4">\n                <img src="{{ alerte\.image\.url }}" alt="{{ alerte\.title }}" class="w-full h-auto object-cover max-h-48">\n            </div>\n            {% endif %}\n'
content = re.sub(img_pattern, '', content)

with open('templates/app_mobile/alertes.html', 'w', encoding='utf-8') as f:
    f.write(content)
