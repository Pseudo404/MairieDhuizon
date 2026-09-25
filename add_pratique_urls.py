with open('mairieDhuizon/urls.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "path('app/pratique/', views_app_mobile.app_pratique, name='app_pratique'),",
    """path('app/pratique/', views_app_mobile.app_pratique, name='app_pratique'),
    path('app/pratique/dechets/', views_app_mobile.app_pratique_dechets, name='app_pratique_dechets'),
    path('app/pratique/sante/', views_app_mobile.app_pratique_sante, name='app_pratique_sante'),
    path('app/pratique/ecole/', views_app_mobile.app_pratique_ecole, name='app_pratique_ecole'),
    path('app/pratique/mairie/', views_app_mobile.app_pratique_mairie, name='app_pratique_mairie'),"""
)

with open('mairieDhuizon/urls.py', 'w', encoding='utf-8') as f:
    f.write(content)
