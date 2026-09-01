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


def send_periscolaire_email(data):
    """
    Envoie l'inscription périscolaire (Garderie / Cantine) à la mairie
    et un accusé de réception au parent.
    data : dict issu du formulaire InscriptionPeriscolaireForm.cleaned_data
    """
    if not settings.BREVO_API_KEY:
        logger.error("BREVO_API_KEY non configurée. Email périscolaire non envoyé.")
        return False, "Le service d'envoi d'emails n'est pas configuré."

    api_instance = _get_api_instance()

    enfant_fullname = f"{escape(data.get('prenom_enfant', ''))} {escape(data.get('nom_enfant', ''))}"
    parent_nom = sanitize_email_header(data.get('responsable_1_nom_prenom', ''), 100)

    def row(label, value):
        if not value:
            val = '<em style="color:#aaa;">Non renseigné</em>'
        else:
            if hasattr(value, 'strftime'):
                if type(value).__name__ == 'date':
                    val = escape(value.strftime('%d/%m/%Y'))
                elif type(value).__name__ == 'time':
                    val = escape(value.strftime('%H:%M'))
                else:
                    val = escape(str(value))
            else:
                val = escape(str(value))
        return f'<tr><td style="padding:8px 12px;font-weight:600;color:#15803d;width:220px;vertical-align:top;">{label}</td><td style="padding:8px 12px;">{val}</td></tr>'

    def section(title, icon=""):
        return f'''
        <tr><td colspan="2" style="padding:16px 12px 8px;background:#f0fdf4;font-size:15px;font-weight:700;color:#14532d;border-top:2px solid #bbf7d0;">
            <span style="margin-right:6px;">{icon}</span>{title}
        </td></tr>'''

    def check(val):
        return "✔️" if val else "—"

    grid_html = f"""
    <tr><td colspan="2" style="padding: 0;">
    <table style="width:100%; border-collapse:collapse; margin: 15px 0;">
        <tr style="background:#d9e1f2;">
            <th style="padding:8px;border:1px solid #ccc;font-size:12px;">Service</th>
            <th style="padding:8px;border:1px solid #ccc;font-size:12px;">Lundi</th>
            <th style="padding:8px;border:1px solid #ccc;font-size:12px;">Mardi</th>
            <th style="padding:8px;border:1px solid #ccc;font-size:12px;">Mercredi</th>
            <th style="padding:8px;border:1px solid #ccc;font-size:12px;">Jeudi</th>
            <th style="padding:8px;border:1px solid #ccc;font-size:12px;">Vendredi</th>
            <th style="padding:8px;border:1px solid #ccc;font-size:12px;">Régulier</th>
            <th style="padding:8px;border:1px solid #ccc;font-size:12px;">Occasionnel</th>
        </tr>
        <tr>
            <td style="padding:8px;border:1px solid #ccc;font-size:12px;font-weight:bold;">Garderie matin</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('gm_lundi'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('gm_mardi'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('gm_mercredi'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('gm_jeudi'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('gm_vendredi'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('gm_regulier'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('gm_occasionnel'))}</td>
        </tr>
        <tr>
            <td style="padding:8px;border:1px solid #ccc;font-size:12px;font-weight:bold;">Cantine</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('can_lundi'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('can_mardi'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('can_mercredi'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('can_jeudi'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('can_vendredi'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('can_regulier'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('can_occasionnel'))}</td>
        </tr>
        <tr>
            <td style="padding:8px;border:1px solid #ccc;font-size:12px;font-weight:bold;">Garderie soir</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('gs_lundi'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('gs_mardi'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('gs_mercredi'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('gs_jeudi'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('gs_vendredi'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('gs_regulier'))}</td>
            <td style="padding:8px;border:1px solid #ccc;text-align:center;">{check(data.get('gs_occasionnel'))}</td>
        </tr>
    </table>
    </td></tr>
    """

    html_rows = f"""
    {section("Renseignements de l'enfant", "👧")}
    {row("Nom", data.get('nom_enfant'))}
    {row("Prénom", data.get('prenom_enfant'))}
    {row("Date de naissance", data.get('date_naissance_enfant'))}
    {row("Classe", data.get('classe_enfant'))}

    {section("Responsables légaux", "👤")}
    {row("Responsable 1", data.get('responsable_1_nom_prenom'))}
    {row("Adresse 1", data.get('responsable_1_adresse'))}
    {row("Téléphone 1", data.get('responsable_1_telephone'))}
    {row("Courriel 1", data.get('responsable_1_courriel'))}
    <tr><td colspan="2"><hr style="border:0;border-top:1px dashed #ccc;margin:5px 0;"></td></tr>
    {row("Responsable 2", data.get('responsable_2_nom_prenom'))}
    {row("Adresse 2", data.get('responsable_2_adresse'))}
    {row("Téléphone 2", data.get('responsable_2_telephone'))}
    {row("Courriel 2", data.get('responsable_2_courriel'))}

    {section("Responsable financier", "💰")}
    {row("Nom et Prénom", data.get('responsable_financier'))}
    {row("Adresse", data.get('responsable_financier_adresse'))}

    {section("Service demandé", "📋")}
    {grid_html}
    {row("Heure habituelle d'arrivée", data.get('heure_arrivee'))}
    {row("Heure habituelle de départ", data.get('heure_depart'))}

    {section("Santé et restauration", "🏥")}
    {row("PAI en cours", data.get('pai_en_cours'))}
    {row("Allergies / Consignes", data.get('allergies'))}

    {section("Personnes à prévenir en cas d'urgence", "📞")}
    {row("Nom et prénom", data.get('urgence_nom_prenom'))}
    {row("Lien avec l'enfant", data.get('urgence_lien'))}
    {row("Téléphone", data.get('urgence_telephone'))}

    {section("Assurance extra-scolaire", "🛡️")}
    {row("Coordonnées de l'assurance", data.get('assurance_coordonnees'))}
    {row("Souscripteur", data.get('assurance_souscripteur'))}
    {row("Numéro de contrat", data.get('assurance_numero'))}

    {section("Personnes autorisées (hors responsables)", "✅")}
    {row("Personne 1", data.get('auth_1'))}
    {row("Personne 2", data.get('auth_2'))}

    {section("Engagement du responsable légal", "✍️")}
    {row("Signataire", data.get('soussigne'))}
    {row("Fait à", data.get('fait_a'))}
    {row("Le", data.get('le_date'))}
    {row("Certification exactitude", check(data.get('engagement_certifie')))}
    {row("Règlement cantine", check(data.get('engagement_cantine')))}
    {row("Règlement garderie", check(data.get('engagement_garderie')))}
    """

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; max-width: 680px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #14532d, #15803d); padding: 30px; border-radius: 12px 12px 0 0;">
            <h1 style="color: #fff; margin: 0; font-size: 20px;">📝 Fiche d'inscription aux services périscolaires</h1>
            <p style="color: #bbf7d0; margin: 8px 0 0; font-size: 14px;">Formulaire soumis depuis le site dhuizon.fr</p>
        </div>
        <div style="background: #fff; border: 1px solid #e0e0e0; border-top: none; border-radius: 0 0 12px 12px; overflow: hidden;">
            <table style="width: 100%; border-collapse: collapse;">
                {html_rows}
            </table>
        </div>
    </body>
    </html>
    """

    # Email vers la mairie
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": emails_config.PERISCOLAIRE_RECEPTION_EMAIL, "name": "Mairie de Dhuizon"}],
        sender={"email": emails_config.MAIRIE_SENDER_EMAIL, "name": emails_config.MAIRIE_SENDER_NAME},
        reply_to={"email": data.get('responsable_1_courriel'), "name": parent_nom},
        subject=f"[Inscription Périscolaire] {enfant_fullname}",
        html_content=html_content,
    )
    try:
        api_instance.send_transac_email(send_smtp_email)
        logger.info("Email inscription périscolaire envoyé pour %s", enfant_fullname)
    except ApiException as e:
        logger.error("Erreur API Brevo (périscolaire): %s", e)
        return False, "Une erreur est survenue lors de l'envoi. Veuillez réessayer."
    except Exception as e:
        logger.error("Erreur inattendue (périscolaire): %s", e)
        return False, "Une erreur inattendue est survenue."

    # Accusé de réception au parent
    parent_prenom = escape(data.get('responsable_1_nom_prenom', '').split()[0] if data.get('responsable_1_nom_prenom') else '')
    confirmation_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #14532d, #15803d); padding: 30px; border-radius: 12px 12px 0 0;">
            <h1 style="color: #fff; margin: 0; font-size: 22px;">Demande d'inscription reçue ✅</h1>
        </div>
        <div style="background: #fff; padding: 30px; border: 1px solid #e0e0e0; border-top: none; border-radius: 0 0 12px 12px;">
            <p style="font-size: 16px;">Bonjour <strong>{parent_prenom}</strong>,</p>
            <p style="font-size: 16px; line-height: 1.6;">
                Nous avons bien reçu votre fiche d'inscription aux services périscolaires
                pour <strong>{enfant_fullname}</strong>.<br>
                Notre équipe la traitera dans les meilleurs délais et vous contactera si nécessaire.
            </p>
            <p style="font-size: 14px; color: #666;">
                Cordialement,<br><strong>La Mairie de Dhuizon</strong>
            </p>
            <p style="margin-top: 20px; font-size: 12px; color: #888;">
                Ceci est un accusé de réception automatique, merci de ne pas y répondre directement.
            </p>
        </div>
    </body>
    </html>
    """
    if data.get('responsable_1_courriel'):
        confirmation_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": data.get('responsable_1_courriel'), "name": parent_nom}],
            sender={"email": emails_config.MAIRIE_SENDER_EMAIL, "name": emails_config.MAIRIE_SENDER_NAME},
            subject="Mairie de Dhuizon — Votre inscription périscolaire a bien été reçue",
            html_content=confirmation_html,
        )
        try:
            api_instance.send_transac_email(confirmation_email)
            logger.info("Accusé de réception périscolaire envoyé à %s", data.get('responsable_1_courriel'))
        except Exception as e:
            logger.warning("Accusé de réception périscolaire non envoyé: %s", e)

    return True, None

