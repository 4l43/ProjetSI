import smtplib
from email.message import EmailMessage

# Email file path
textfile = "example.txt"  # Replace this with your text file path

# Email details
sender_email = "u41005688@gmail.com"
recipient_email = "41005688@parisnanterre.fr"
password = "1618"  # Use an App Password, not your Gmail password

# Create the email message
msg = EmailMessage()
with open(textfile) as fp:
    msg.set_content(fp.read())

msg['Subject'] = f'The contents of {textfile}'
msg['From'] = sender_email
msg['To'] = recipient_email

# Sending the email via Gmail's SMTP server
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)
        print("Email sent successfully!")
except Exception as e:
    print(f"An error occurred: {e}")
