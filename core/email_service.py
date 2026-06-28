import logging
from django.conf import settings
from django.utils.html import escape
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from core.validators import sanitize_email_header

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
        to=[{"email": settings.BREVO_RECIPIENT_EMAIL, "name": "Mairie de Dhuizon"}],
        sender={"email": settings.BREVO_SENDER_EMAIL, "name": settings.BREVO_SENDER_NAME},
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
        sender={"email": settings.BREVO_SENDER_EMAIL, "name": settings.BREVO_SENDER_NAME},
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
