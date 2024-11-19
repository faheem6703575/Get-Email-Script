import imaplib
import email
from email.header import decode_header
import os

username = "Placed Your Gmail"

password = "Placed Your Gmail Aap password not a actual password"

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username, password)
mail.select("inbox")

status, messages = mail.search(None, 'ALL')
messages = messages[0].split(b' ')

for mail_number in messages:
    status, msg_data = mail.fetch(mail_number, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')
            from_ = msg.get("From")
            print("Subject:", subject)
            print("From:", from_)

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename and filename.endswith(".pdf"):
                            if not os.path.isdir("attachments"):
                                os.mkdir("attachments")
                            filepath = os.path.join("attachments", filename)
                            open(filepath, "wb").write(part.get_payload(decode=True))
                            print(f"Downloaded {filename} to attachments folder")

mail.close()
mail.logout()