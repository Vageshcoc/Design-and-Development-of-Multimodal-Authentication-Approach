import smtplib
import pyttsx3
engine = pyttsx3.init()



def send_otp_email(otp,receiver_email):
    # Sender's email configuration
    sender_email = "pushpampushpam618@gmail.com"  # Replace with your email
    sender_password = "isxemngswyykspge"  # Replace with your email password

    # SMTP server configuration (for Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create an SMTP session
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Start TLS for security

    try:
        # Log in to the email account
        server.login(sender_email, sender_password)

        # Email content
        subject = "Your OTP"
        body = f"Your OTP is: {otp}"
        message = f"Subject: {subject}\n\n{body}"

        # Send the email
        server.sendmail(sender_email, receiver_email, message)
        print("OTP sent successfully!")

    except Exception as e:
        print("Error:", e)
        engine.say("Could not send otp, check your internet connection")
        engine.runAndWait()

    finally:
        # Quit the SMTP session
        server.quit()
        engine.say("Otp sent to your email")
        engine.runAndWait()

# Example usage:
#email_address = "recipient@example.com"  # Replace with the recipient's email address
#otp = generate_otp()
#send_otp_email(email_address, otp)
