import re

with open('templates/app_mobile/accueil.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the header
old_header_regex = r'<div class="safe-top bg-green-600 text-white rounded-b-3xl shadow-md pb-6 pt-12 px-6">.*?</div>\n</div>'
new_header = """<div class="safe-top bg-green-600 rounded-b-3xl shadow-md pb-6 pt-12 px-6 flex justify-center items-center">
    {% if site_logo_url %}
        <img src="{{ site_logo_url }}" alt="Mairie de Dhuizon" class="h-24 w-auto object-contain drop-shadow-md">
    {% else %}
        <img src="{% static 'images/logo-dhuizon.webp' %}" alt="Mairie de Dhuizon" class="h-24 w-auto object-contain drop-shadow-md">
    {% endif %}
</div>"""

content = re.sub(old_header_regex, new_header, content, flags=re.DOTALL)

# Replace the news items loop
old_news_regex = r'{% for alerte in alertes %}\n\s*<div class="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 border-l-4.*?</div>'

new_news = """{% for alerte in alertes %}
        <a href="{% url 'actualite_detail' news_id=alerte.id %}" class="block bg-white p-4 rounded-2xl shadow-sm border border-gray-100 border-l-4 {% if 'alerte' in alerte.title|lower %}border-l-red-500{% else %}border-l-green-500{% endif %} active:scale-[0.98] transition-transform">
            <p class="text-xs text-gray-400 font-semibold mb-1">{{ alerte.created_at|date:"d M Y" }}</p>
            <h3 class="font-bold text-gray-800">{{ alerte.title }}</h3>
            {% if alerte.image %}
            <div class="mt-3 rounded-xl overflow-hidden h-32 relative mb-2">
                <img src="{{ alerte.image.url }}" alt="{{ alerte.title }}" class="w-full h-full object-cover">
            </div>
            {% endif %}
            <p class="text-gray-600 text-sm mt-2 line-clamp-3">{{ alerte.content }}</p>
            <div class="text-green-600 text-xs font-semibold mt-3 flex items-center justify-end">
                Lire la suite <span class="text-lg leading-none ml-1">&#8250;</span>
            </div>
        </a>"""

content = re.sub(old_news_regex, new_news, content, flags=re.DOTALL)

with open('templates/app_mobile/accueil.html', 'w', encoding='utf-8') as f:
    f.write(content)
