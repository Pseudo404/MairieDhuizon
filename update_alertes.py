import re

with open('templates/app_mobile/alertes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the title to "Actualités & Alertes"
content = content.replace(
    '<h1 class="text-2xl font-bold text-gray-900">Alertes & Infos</h1>',
    '<h1 class="text-2xl font-bold text-gray-900">Actualités & Infos</h1>'
)

# Replace the news item loop
old_news_regex = r'{% for alerte in alertes %}\n\s*<div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 border-l-4.*?</div>\n        </div>'

new_news = """{% for alerte in alertes %}
        <a href="{% url 'actualite_detail' news_id=alerte.id %}" class="block bg-white p-5 rounded-2xl shadow-sm border border-gray-100 border-l-4 {% if 'alerte' in alerte.title|lower %}border-l-red-500{% else %}border-l-green-500{% endif %} active:scale-[0.98] transition-transform">
            <p class="text-xs text-gray-400 font-semibold mb-1">{{ alerte.created_at|date:"d M Y - H:i" }}</p>
            <h3 class="font-bold text-gray-800 text-lg mb-2">{{ alerte.title }}</h3>
            {% if alerte.image %}
            <div class="mt-3 rounded-xl overflow-hidden relative mb-4">
                <img src="{{ alerte.image.url }}" alt="{{ alerte.title }}" class="w-full h-auto object-cover max-h-48">
            </div>
            {% endif %}
            <div class="text-gray-600 text-sm leading-relaxed prose prose-sm line-clamp-4">
                {{ alerte.content|safe|linebreaks }}
            </div>
            <div class="text-green-600 text-sm font-semibold mt-4 flex items-center justify-end">
                Lire la suite <span class="text-xl leading-none ml-1">&#8250;</span>
            </div>
        </a>"""

content = re.sub(old_news_regex, new_news, content, flags=re.DOTALL)

with open('templates/app_mobile/alertes.html', 'w', encoding='utf-8') as f:
    f.write(content)
