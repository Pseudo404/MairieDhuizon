with open('core/email_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''    attachments = []
    if piece_jointe:
        try:
            import base64
            b64_content = base64.b64encode(piece_jointe.read()).decode('utf-8')
            attachments.append({
                "content": b64_content,
                "name": piece_jointe.name
            })
        except Exception as e:
            logger.error(f"Erreur d'encodage pi\u00e8ce jointe: {e}")'''

new = '''    attachments = []
    if piece_jointe:
        try:
            import base64
            b64_content = base64.b64encode(piece_jointe.read()).decode('utf-8')
            attachments.append(
                sib_api_v3_sdk.SendSmtpEmailAttachment(
                    content=b64_content,
                    name=piece_jointe.name
                )
            )
        except Exception as e:
            logger.error(f"Erreur d\'encodage piece jointe: {e}")'''

if old in content:
    content = content.replace(old, new)
    with open('core/email_service.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS")
else:
    # try exact bytes match
    with open('core/email_service.py', 'rb') as f:
        raw = f.read()
    print("Not found. Searching for 'attachments.append'...")
    idx = raw.find(b'attachments.append({')
    print(f"Found at byte: {idx}")
    if idx != -1:
        chunk = raw[max(0,idx-5):idx+200]
        print(repr(chunk))
