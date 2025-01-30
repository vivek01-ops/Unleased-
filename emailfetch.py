import imaplib
import email
import yaml  # To load saved login credentials from a yaml file

def fetch_emails():
    # Load credentials
    with open("D:/ML projects/Campus Collab HUB/credentials.yaml") as f:
        content = f.read()

    my_credentials = yaml.load(content, Loader=yaml.FullLoader)

    # Load the user name and password from the yaml file
    user, password = my_credentials["user"], my_credentials["password"]

    # URL for IMAP connection
    imap_url = 'imap.gmail.com'

    # Connection with GMAIL using SSL
    my_mail = imaplib.IMAP4_SSL(imap_url)

    # Log in using your credentials
    my_mail.login(user, password)

    # Select the Inbox to fetch messages
    my_mail.select('Inbox')

    # Define list of senders (multiple values)
    senders_list = ['monika@lilapoonawallafoundation.com']

    # Empty list to store all message IDs
    all_msgs = []

    # Iterate over the senders list
    for sender in senders_list:
        key = 'FROM'
        value = sender
        _, data = my_mail.search(None, key, value)

        mail_id_list = data[0].split()  # IDs of all emails that we want to fetch
        all_msgs.extend(mail_id_list)

    # Fetch emails and return them
    emails = []
    for num in all_msgs:
        typ, data = my_mail.fetch(num, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                my_msg = email.message_from_bytes(response_part[1])
                email_data = {
                    "subject": my_msg["subject"],
                    "from": my_msg["from"],
                    "body": ""
                }

                # Extract body text
                for part in my_msg.walk():
                    if part.get_content_type() == 'text/plain':
                        email_data["body"] = part.get_payload()

                emails.append(email_data)

    # Return the list of email objects
    return emails
