import re

with open('templates/app_mobile/accueil.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the header logo
old_header = r'<div class="safe-top bg-green-600 rounded-b-3xl shadow-md pb-6 pt-12 px-6 flex justify-center items-center">.*?</div>\n</div>'
new_header = """<div class="safe-top bg-green-600 rounded-b-3xl shadow-md pb-5 pt-10 px-6 flex justify-center items-center">
    <div class="bg-white p-3 rounded-2xl shadow-sm">
        {% if site_logo_url %}
            <img src="{{ site_logo_url }}" alt="Mairie de Dhuizon" class="h-12 w-auto object-contain">
        {% else %}
            <img src="{% static 'images/logo-dhuizon.webp' %}" alt="Mairie de Dhuizon" class="h-12 w-auto object-contain">
        {% endif %}
    </div>
</div>"""

content = re.sub(old_header, new_header, content, flags=re.DOTALL)

# Remove the image from the news items
img_pattern = r'            {% if alerte\.image %}\n            <div class="mt-3 rounded-xl overflow-hidden h-32 relative mb-2">\n                <img src="{{ alerte\.image\.url }}" alt="{{ alerte\.title }}" class="w-full h-full object-cover">\n            </div>\n            {% endif %}\n'
content = re.sub(img_pattern, '', content)

with open('templates/app_mobile/accueil.html', 'w', encoding='utf-8') as f:
    f.write(content)
