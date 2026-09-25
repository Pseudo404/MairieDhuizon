import re

with open('templates/app_mobile/base_app.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = """
    <link rel="manifest" href="{% url 'manifest_json' %}">
    {% if site_logo_url %}
        <link rel="apple-touch-icon" href="{{ site_logo_url }}">
    {% else %}
        <link rel="apple-touch-icon" href="{% static 'images/logo-dhuizon.webp' %}">
    {% endif %}
"""

content = re.sub(
    r'<link rel="manifest" href="{% url \'manifest_json\' %}">\n\s*<link rel="apple-touch-icon" href="{% static \'images/logo-dhuizon\.webp\' %}">',
    replacement.strip('\n'),
    content
)

with open('templates/app_mobile/base_app.html', 'w', encoding='utf-8') as f:
    f.write(content)
