import imaplib
import email
from email.header import decode_header

# Configuration Constants
EMAIL_SERVER = "imap.gmail.com"  # IMAP server for your email provider
EMAIL_ADDRESS = "diegorosario2013@gmail.com"  # Replace with your email address
EMAIL_PASSWORD = "gump kxdq eils osje"  # Replace with your email password

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

# Function to fetch the latest email
def fetch_latest_email(mail):
    try:
        # Select the inbox
        mail.select("inbox")

        # Search for all emails
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            print("No emails found!")
            return None

        # Get the latest email ID
        message_ids = messages[0].split()
        latest_email_id = message_ids[-1]

        # Fetch the email
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        if status != "OK":
            print("Failed to fetch the email!")
            return None

        # Parse the email
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                sender = msg.get("From")
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            return subject, sender, body
                else:
                    body = msg.get_payload(decode=True).decode()
                    return subject, sender, body
        return None
    except Exception as e:
        print(f"Error fetching the latest email: {e}")
        return None

# Main function
def main():
    # Connect to the email server
    mail = connect_email(EMAIL_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD)
    if not mail:
        return

    # Fetch and display the latest email
    email_data = fetch_latest_email(mail)
    if email_data:
        subject, sender, body = email_data
        print("Subject:", subject)
        print("Sender:", sender)
        print("Body:", body)
    else:
        print("No email data retrieved.")

    # Logout from the email server
    mail.logout()

# Run the program
if __name__ == "__main__":
    main()

