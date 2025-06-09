import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient_email, subject, message):
    sender_email = "laptopuse01824x@gmail.com"  # Your Gmail ID
    sender_password = "ghcm oafn ilde vfna"  # Use an App Password for security
    sender_name = "Team Insta"  # Change this to any name you want

    msg = MIMEMultipart()
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    recipient = input("jatinsharma23558@gmail.com")
    subject = input("Your Account is Under Review for Policy Violations: ")
    message = input("""Dear Jatin Sharma,

                    We have received multiple reports regarding your account @ja.tin_____ on Instagram. Our moderation team is currently reviewing these reports to ensure compliance with our community guidelines.

                    If our investigation confirms any violations, your account may be temporarily or permanently suspended. To avoid this, we request you to review our Community Guidelines and ensure that your activities comply with our policies.

                    If you believe this action was taken in error, you may appeal by responding to this email within 24 Hours with a valid explanation.

                    Best regards,
                    Michael, Cyber Support
                    Instagram Support team Support Team
                    jatinsharma23558@gmail.com""")
    
    send_email(recipient, subject, message)
