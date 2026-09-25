import re

with open('mairieDhuizon/urls.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "path('app/alertes/', views_app_mobile.app_alertes, name='app_alertes'),",
    "path('app/alertes/', views_app_mobile.app_alertes, name='app_alertes'),\n    path('app/actualite/<int:news_id>/', views_app_mobile.app_actualite_detail, name='app_actualite_detail'),"
)

with open('mairieDhuizon/urls.py', 'w', encoding='utf-8') as f:
    f.write(content)
