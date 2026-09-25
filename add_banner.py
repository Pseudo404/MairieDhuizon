import re
with open('templates/panel/app_mobile/signalements.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_content = re.sub(
    r'(\{% endif %\})\n\n    (\{# .*? Filtres .*? #\})',
    r'\1\n\n    <div class="bg-blue-50 border-l-4 border-blue-500 text-blue-800 p-4 rounded-r-xl mb-6 shadow-sm">\n        <p class="font-bold text-sm">&#9432; Nettoyage automatique activé</p>\n        <p class="text-sm mt-1">Les signalements ayant le statut <strong>Résolu</strong> ou <strong>Rejeté</strong> sont automatiquement supprimés du serveur (avec leurs photos) au bout de 7 jours pour libérer de l\'espace.</p>\n    </div>\n\n    \2',
    content
)

with open('templates/panel/app_mobile/signalements.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
