import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = """
    {% if site_logo_url %}
        <link rel="icon" href="{{ site_logo_url }}">
        <link rel="apple-touch-icon" href="{{ site_logo_url }}">
        <meta property="og:image" content="{{ request.scheme }}://{{ request.get_host }}{{ site_logo_url }}">
    {% else %}
        <link rel="icon" type="image/x-icon" href="{% static 'images/logo-dhuizon.webp' %}">
        <link rel="apple-touch-icon" href="{% static 'images/logo-dhuizon.webp' %}">
        <meta property="og:image" content="{{ request.scheme }}://{{ request.get_host }}{% static 'images/logo-dhuizon.webp' %}">
    {% endif %}
"""

# Replace the single line link rel="icon"...
content = re.sub(
    r'<link rel="icon"[^>]*?href="{% static \'images/logo-dhuizon\.webp\' %}"[^>]*?>',
    replacement.strip('\n'),
    content
)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
