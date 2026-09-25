import re

with open('templates/contact.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add enctype
content = content.replace(
    '<form method="POST" action="{% url \'contact\' %}" class="p-8 lg:p-10 space-y-8">',
    '<form method="POST" action="{% url \'contact\' %}" enctype="multipart/form-data" class="p-8 lg:p-10 space-y-8">'
)

piece_jointe_html = """
                <div>
                    <label for="id_piece_jointe" class="block text-sm font-semibold text-gray-700 mb-2">Pièce jointe (Optionnel)</label>
                    <div class="text-xs text-gray-500 mb-2">Taille maximale : 5 Mo. Formats acceptés : Images, PDF, Word.</div>
                    {{ form.piece_jointe }}
                    {% if form.piece_jointe.errors %}
                        <p class="mt-1 text-sm text-red-600">{{ form.piece_jointe.errors.0 }}</p>
                    {% endif %}
                </div>
"""

# Insert piece_jointe before verification
content = re.sub(
    r'(                <div>\n                    <label for="id_verification")',
    piece_jointe_html.lstrip('\n') + r'\1',
    content
)

with open('templates/contact.html', 'w', encoding='utf-8') as f:
    f.write(content)
