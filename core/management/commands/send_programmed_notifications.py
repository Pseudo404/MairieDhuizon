from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import AppNotification

class Command(BaseCommand):
    help = 'Envoie les notifications programmées'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        notifications = AppNotification.objects.filter(
            est_envoye=False,
            date_programmee__isnull=False,
            date_programmee__lte=now
        )
        
        count = 0
        for notif in notifications:
            # Ici on insèrerait le code d'envoi réel (FCM, OneSignal, etc.)
            # send_push_notification(notif.titre, notif.message, notif.lien)
            
            notif.est_envoye = True
            notif.date_envoi = now
            notif.save()
            count += 1
            self.stdout.write(self.style.SUCCESS(f'Notification envoyée : {notif.titre}'))
            
        if count == 0:
            self.stdout.write('Aucune notification programmée en attente.')
        else:
            self.stdout.write(self.style.SUCCESS(f'{count} notification(s) envoyée(s) avec succès !'))
