import imaplib
import email
from email.header import decode_header

# Configuration Constants
EMAIL_SERVER = "imap.gmail.com"  # IMAP server for Gmail
EMAIL_ADDRESS = "diegorosario2013@gmail.com"  # Replace with your email address
EMAIL_PASSWORD = "gump kxdq eils osje"  # Replace with your Gmail App Password
SUBJECT_FILTER = "Constancia de Pago Plin"  # Subject to filter by
EMAIL_LIMIT = 3  # Number of recent emails to process

# Function to connect to an email account
def connect_email(server, username, password):
    try:
        mail = imaplib.IMAP4_SSL(server)
        mail.login(username, password)
        print("Connected to the email server.")
        return mail
    except Exception as e:
        print(f"Error connecting to the email server: {e}")
        return None

# Function to fetch emails with the specified subject
def fetch_emails_with_subject(mail, subject_filter, limit):
    try:
        # Select the inbox
        mail.select("inbox")

        # Search for emails containing the subject
        status, messages = mail.search(None, f'SUBJECT "{subject_filter}"')
        if status != "OK":
            print("No emails found with the specified subject!")
            return []

        # Get the email IDs
        message_ids = messages[0].split()

        # Limit the number of emails to process
        emails_to_fetch = message_ids[-limit:] if limit > 0 else message_ids

        email_data = []
        for email_id in emails_to_fetch:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            if status != "OK":
                print(f"Failed to fetch email ID {email_id.decode()}")
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    sender = msg.get("From")
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            try:
                                if content_type == "text/plain":
                                    body += part.get_payload(decode=True).decode()
                                elif content_type == "text/html":
                                    body += part.get_payload(decode=True).decode()
                            except:
                                pass  # Handle unexpected encoding errors
                    else:
                        try:
                            body = msg.get_payload(decode=True).decode()
                        except:
                            pass
                    email_data.append({"subject": subject, "sender": sender, "body": body})
        return email_data
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []

# Main function
def main():
    # Connect to the email server
    mail = connect_email(EMAIL_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD)
    if not mail:
        return

    # Fetch and display the emails
    emails = fetch_emails_with_subject(mail, SUBJECT_FILTER, EMAIL_LIMIT)
    if emails:
        for idx, email_data in enumerate(emails, start=1):
            print(f"\n--- Email {idx} ---")
            print(f"Subject: {email_data['subject']}")
            print(f"Sender: {email_data['sender']}")
            print(f"Body:\n{email_data['body']}")
    else:
        print("No emails retrieved.")

    # Logout from the email server
    mail.logout()

# Run the program
if __name__ == "__main__":
    main()

