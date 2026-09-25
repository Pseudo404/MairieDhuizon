import re

with open('core/email_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace definition
content = re.sub(
    r'def send_contact_email\(nom, prenom, email, telephone, objet, message\):',
    r'def send_contact_email(nom, prenom, email, telephone, objet, message, piece_jointe=None):',
    content
)

# Find where send_smtp_email is instantiated
send_smtp_email_pattern = r'send_smtp_email = sib_api_v3_sdk\.SendSmtpEmail\((.*?)\)'

new_code = """
    attachments = []
    if piece_jointe:
        try:
            import base64
            b64_content = base64.b64encode(piece_jointe.read()).decode('utf-8')
            attachments.append({
                "content": b64_content,
                "name": piece_jointe.name
            })
        except Exception as e:
            logger.error(f"Erreur d'encodage pièce jointe: {e}")

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": emails_config.MAIRIE_CONTACT_RECEPTION_EMAIL, "name": "Mairie de Dhuizon"}],
        sender={"email": emails_config.MAIRIE_SENDER_EMAIL, "name": emails_config.MAIRIE_SENDER_NAME},
        reply_to={"email": email, "name": sanitize_email_header(f"{prenom} {nom}", 100)},
        subject=f"[Contact Mairie] {objet_subject}",
        html_content=html_content,
        attachment=attachments if attachments else None
    )
"""

content = re.sub(
    r'    send_smtp_email = sib_api_v3_sdk\.SendSmtpEmail\([\s\S]*?html_content=html_content,\n    \)',
    new_code.strip('\n'),
    content
)

with open('core/email_service.py', 'w', encoding='utf-8') as f:
    f.write(content)
