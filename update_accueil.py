import re

with open('templates/app_mobile/accueil.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Quick Actions grid
new_grid = """
    <div class="grid grid-cols-2 gap-4">
        <a href="{% url 'app_signalement' %}" class="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex flex-col items-center text-center active:scale-95 transition-transform">
            <span class="text-3xl mb-2">&#128248;</span>
            <span class="font-semibold text-gray-700">Signaler</span>
        </a>
        <button onclick="document.getElementById('contact-modal').classList.remove('hidden')" class="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex flex-col items-center text-center active:scale-95 transition-transform w-full">
            <span class="text-3xl mb-2">&#128222;</span>
            <span class="font-semibold text-gray-700">Contacter</span>
        </button>
        <a href="{% url 'app_alertes' %}" class="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex flex-col items-center text-center active:scale-95 transition-transform">
            <span class="text-3xl mb-2">&#128227;</span>
            <span class="font-semibold text-gray-700">Dernières actualités</span>
        </a>
        <a href="{% url 'app_pratique' %}" class="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex flex-col items-center text-center active:scale-95 transition-transform">
            <span class="text-3xl mb-2">&#128204;</span>
            <span class="font-semibold text-gray-700">Pratique</span>
        </a>
    </div>
"""

# Find the grid in the original file
content = re.sub(
    r'<div class="grid grid-cols-2 gap-4">.*?</div>\s*<!-- Alertes',
    new_grid.strip() + '\n\n    <!-- Alertes',
    content,
    flags=re.DOTALL
)

# Also replace the header for Alertes récentes
content = content.replace(
    'Dernires informations',
    'Dernières actualités'
).replace(
    'Dernières informations',
    'Dernières actualités'
)

# Add the modal at the bottom before {% endblock %}
modal_html = """
<!-- Contact Modal -->
<div id="contact-modal" class="fixed inset-0 bg-black bg-opacity-50 z-50 hidden flex items-center justify-center px-4 transition-opacity">
    <div class="bg-white rounded-3xl w-full max-w-sm p-6 shadow-xl transform transition-all">
        <div class="flex justify-between items-center mb-6">
            <h3 class="text-xl font-bold text-gray-800">Contacter la mairie</h3>
            <button onclick="document.getElementById('contact-modal').classList.add('hidden')" class="text-gray-400 hover:text-gray-600">
                <span class="text-2xl">&times;</span>
            </button>
        </div>
        
        <div class="space-y-4">
            <a href="tel:0254764422" class="w-full flex items-center gap-4 bg-green-50 p-4 rounded-2xl active:bg-green-100 transition-colors">
                <div class="bg-green-500 text-white p-3 rounded-xl">
                    <span class="text-xl">&#128222;</span>
                </div>
                <div>
                    <div class="font-bold text-green-900">Appeler</div>
                    <div class="text-sm text-green-700">02 54 76 44 22</div>
                </div>
            </a>
            
            <a href="{% url 'contact' %}" class="w-full flex items-center gap-4 bg-blue-50 p-4 rounded-2xl active:bg-blue-100 transition-colors">
                <div class="bg-blue-500 text-white p-3 rounded-xl">
                    <span class="text-xl">&#9993;</span>
                </div>
                <div>
                    <div class="font-bold text-blue-900">Formulaire de contact</div>
                    <div class="text-sm text-blue-700">Envoyer un e-mail</div>
                </div>
            </a>
        </div>
        
        <button onclick="document.getElementById('contact-modal').classList.add('hidden')" class="mt-6 w-full py-3 bg-gray-100 text-gray-700 font-semibold rounded-xl active:bg-gray-200">
            Annuler
        </button>
    </div>
</div>
"""

content = content.replace('{% endblock %}', modal_html + '\n{% endblock %}')

with open('templates/app_mobile/accueil.html', 'w', encoding='utf-8') as f:
    f.write(content)
