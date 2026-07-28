import logging
from django.conf import settings
from django.utils.html import escape
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from core.validators import sanitize_email_header
import emails_accounts as emails_config

logger = logging.getLogger(__name__)

def _get_api_instance():
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY
    client = sib_api_v3_sdk.ApiClient(configuration)
    email_api = sib_api_v3_sdk.TransactionalEmailsApi(client)
    return email_api

def send_contact_email(nom, prenom, email, telephone, objet, message):
    if not settings.BREVO_API_KEY:
        logger.error("BREVO_API_KEY non configurée. Email non envoyé.")
        return False, "Le service d'envoi d'emails n'est pas configuré."

    nom = escape(nom)
    prenom = escape(prenom)
    email_display = escape(email)
    telephone = escape(telephone or 'Non renseigné')
    objet_display = escape(objet)
    message = escape(message)
    objet_subject = sanitize_email_header(objet)
    
    api_instance = _get_api_instance()

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #2d6a4f, #40916c); padding: 30px; border-radius: 12px 12px 0 0;">
            <h1 style="color: #fff; margin: 0; font-size: 22px;">Nouveau message — Formulaire de contact</h1>
        </div>
        <div style="background: #fff; padding: 30px; border: 1px solid #e0e0e0; border-top: none; border-radius: 0 0 12px 12px;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="padding: 10px 0; font-weight: bold; color: #2d6a4f; width: 140px;">Nom :</td><td style="padding: 10px 0;">{nom}</td></tr>
                <tr><td style="padding: 10px 0; font-weight: bold; color: #2d6a4f;">Prénom :</td><td style="padding: 10px 0;">{prenom}</td></tr>
                <tr><td style="padding: 10px 0; font-weight: bold; color: #2d6a4f;">Email :</td><td style="padding: 10px 0;">{email_display}</td></tr>
                <tr><td style="padding: 10px 0; font-weight: bold; color: #2d6a4f;">Téléphone :</td><td style="padding: 10px 0;">{telephone}</td></tr>
                <tr><td style="padding: 10px 0; font-weight: bold; color: #2d6a4f;">Objet :</td><td style="padding: 10px 0; font-weight: bold;">{objet_display}</td></tr>
            </table>
            <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
            <h3 style="color: #2d6a4f; margin-bottom: 10px;">Message :</h3>
            <div style="background: #f8faf9; padding: 20px; border-radius: 8px; line-height: 1.6; white-space: pre-wrap;">{message}</div>
            <p style="margin-top: 25px; font-size: 12px; color: #888;">
                Ce message a été envoyé depuis le formulaire de contact du site dhuizon.fr
            </p>
        </div>
    </body>
    </html>
    """

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": emails_config.MAIRIE_CONTACT_RECEPTION_EMAIL, "name": "Mairie de Dhuizon"}],
        sender={"email": emails_config.MAIRIE_SENDER_EMAIL, "name": emails_config.MAIRIE_SENDER_NAME},
        reply_to={"email": email, "name": sanitize_email_header(f"{prenom} {nom}", 100)},
        subject=f"[Contact Mairie] {objet_subject}",
        html_content=html_content,
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        logger.info("Email de contact envoyé avec succès de %s", email)
        return True, None
    except ApiException as e:
        logger.error("Erreur API Brevo lors de l'envoi: %s", e)
        return False, "Une erreur est survenue lors de l'envoi. Veuillez réessayer."
    except Exception as e:
        logger.error("Erreur inattendue lors de l'envoi d'email: %s", e)
        return False, "Une erreur inattendue est survenue. Veuillez réessayer."

def send_confirmation_email(email, prenom):
    if not settings.BREVO_API_KEY:
        return False, "Service d'envoi non configuré."

    prenom = escape(prenom)
    api_instance = _get_api_instance()

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #2d6a4f, #40916c); padding: 30px; border-radius: 12px 12px 0 0;">
            <h1 style="color: #fff; margin: 0; font-size: 22px;">Message bien reçu</h1>
        </div>
        <div style="background: #fff; padding: 30px; border: 1px solid #e0e0e0; border-top: none; border-radius: 0 0 12px 12px;">
            <p style="font-size: 16px; line-height: 1.6;">Bonjour <strong>{prenom}</strong>,</p>
            <p style="font-size: 16px; line-height: 1.6;">
                Nous avons bien reçu votre message et nous vous en remercions.
                Notre équipe le traitera dans les meilleurs délais.
            </p>
            <p style="font-size: 14px; color: #666;">
                Cordialement,<br><strong>La Mairie de Dhuizon</strong>
            </p>
            <p style="margin-top: 20px; font-size: 12px; color: #888;">
                Ceci est un message automatique, merci de ne pas y répondre.
            </p>
        </div>
    </body>
    </html>
    """

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": email, "name": sanitize_email_header(prenom, 100)}],
        sender={"email": emails_config.MAIRIE_SENDER_EMAIL, "name": emails_config.MAIRIE_SENDER_NAME},
        subject="Mairie de Dhuizon — Votre message a bien été reçu",
        html_content=html_content,
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        logger.info("Email de confirmation envoyé à %s", email)
        return True, None
    except ApiException as e:
        logger.error("Erreur API Brevo (confirmation): %s", e)
        return False, str(e)
    except Exception as e:
        logger.error("Erreur inattendue (confirmation): %s", e)
        return False, str(e)

def send_reservation_demande_email(inscription, dates):
    if not settings.BREVO_API_KEY: return False, "API non configurée."
    api_instance = _get_api_instance()
    dates_str = ", ".join([d.strftime('%d/%m/%Y') for d in dates])
    html_content = f"""
    <html><body>
        <h3>Demande de réservation - Centre de loisirs</h3>
        <p>Bonjour {escape(inscription.prenom_responsable_1)},</p>
        <p>Nous avons bien reçu votre demande de réservation pour <strong>{escape(inscription.prenom_enfant)} {escape(inscription.nom_enfant)}</strong> pour les dates suivantes : <strong>{dates_str}</strong>.</p>
        <p>Votre demande est <strong>en attente de validation</strong> par nos équipes. Vous recevrez un nouvel email dès qu'elle sera traitée.</p>
        <p>Cordialement,<br>La Mairie de Dhuizon</p>
    </body></html>
    """
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": inscription.email_1, "name": f"{inscription.prenom_responsable_1} {inscription.nom_responsable_1}"}],
        sender={"email": emails_config.CENTRE_LOISIRS_SENDER_EMAIL, "name": emails_config.CENTRE_LOISIRS_SENDER_NAME},
        subject="[Centre de loisirs] Votre demande de réservation",
        html_content=html_content,
    )
    try:
        api_instance.send_transac_email(send_smtp_email)
        return True, None
    except Exception as e:
        return False, str(e)

def send_reservation_validee_email(reservation, request, message_personnalise=None):
    if not settings.BREVO_API_KEY: return False, "API non configurée."
    api_instance = _get_api_instance()
    inscription = reservation.inscription
    cancel_url = request.build_absolute_uri(f"/centre-loisirs/annulation/{reservation.token_annulation}/")
    
    message_html = ""
    if message_personnalise:
        message_html = f"<p><strong>Message de l'équipe :</strong><br>{escape(message_personnalise)}</p>"
        
    html_content = f"""
    <html><body>
        <h3>Réservation Validée - Centre de loisirs</h3>
        <p>Bonjour {escape(inscription.prenom_responsable_1)},</p>
        <p>Nous avons le plaisir de vous informer que la réservation pour <strong>{escape(inscription.prenom_enfant)} {escape(inscription.nom_enfant)}</strong> pour le <strong>{reservation.date.strftime('%d/%m/%Y')}</strong> a été <strong>validée</strong>.</p>
        {message_html}
        <p>Si vous souhaitez annuler cette réservation, veuillez cliquer sur le lien suivant : <br><a href="{cancel_url}">Annuler la réservation</a></p>
        <p>Cordialement,<br>La Mairie de Dhuizon</p>
    </body></html>
    """
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": inscription.email_1, "name": f"{inscription.prenom_responsable_1} {inscription.nom_responsable_1}"}],
        sender={"email": emails_config.CENTRE_LOISIRS_SENDER_EMAIL, "name": emails_config.CENTRE_LOISIRS_SENDER_NAME},
        subject=f"[Centre de loisirs] Réservation validée ({reservation.date.strftime('%d/%m/%Y')})",
        html_content=html_content,
    )
    try:
        api_instance.send_transac_email(send_smtp_email)
        return True, None
    except Exception as e:
        return False, str(e)

def send_reservation_refusee_email(reservation, motif):
    if not settings.BREVO_API_KEY: return False, "API non configurée."
    api_instance = _get_api_instance()
    inscription = reservation.inscription
    html_content = f"""
    <html><body>
        <h3>Réservation Refusée - Centre de loisirs</h3>
        <p>Bonjour {escape(inscription.prenom_responsable_1)},</p>
        <p>Nous sommes au regret de vous informer que la réservation pour <strong>{escape(inscription.prenom_enfant)} {escape(inscription.nom_enfant)}</strong> pour le <strong>{reservation.date.strftime('%d/%m/%Y')}</strong> n'a pas pu être validée.</p>
        <p>Motif : <strong>{escape(motif)}</strong></p>
        <p>Cordialement,<br>La Mairie de Dhuizon</p>
    </body></html>
    """
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": inscription.email_1, "name": f"{inscription.prenom_responsable_1} {inscription.nom_responsable_1}"}],
        sender={"email": emails_config.CENTRE_LOISIRS_SENDER_EMAIL, "name": emails_config.CENTRE_LOISIRS_SENDER_NAME},
        subject=f"[Centre de loisirs] Réservation refusée ({reservation.date.strftime('%d/%m/%Y')})",
        html_content=html_content,
    )
    try:
        api_instance.send_transac_email(send_smtp_email)
        return True, None
    except Exception as e:
        return False, str(e)

def send_reservation_annulee_email(reservation):
    if not settings.BREVO_API_KEY: return False, "API non configurée."
    api_instance = _get_api_instance()
    inscription = reservation.inscription
    html_content = f"""
    <html><body>
        <h3>Annulation confirmée - Centre de loisirs</h3>
        <p>Bonjour {escape(inscription.prenom_responsable_1)},</p>
        <p>Nous vous confirmons l'annulation de la réservation pour <strong>{escape(inscription.prenom_enfant)} {escape(inscription.nom_enfant)}</strong> pour le <strong>{reservation.date.strftime('%d/%m/%Y')}</strong>.</p>
        <p>Cordialement,<br>La Mairie de Dhuizon</p>
    </body></html>
    """
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": inscription.email_1, "name": f"{inscription.prenom_responsable_1} {inscription.nom_responsable_1}"}],
        sender={"email": emails_config.CENTRE_LOISIRS_SENDER_EMAIL, "name": emails_config.CENTRE_LOISIRS_SENDER_NAME},
        subject=f"[Centre de loisirs] Annulation confirmée ({reservation.date.strftime('%d/%m/%Y')})",
        html_content=html_content,
    )
    try:
        api_instance.send_transac_email(send_smtp_email)
        return True, None
    except Exception as e:
        return False, str(e)
