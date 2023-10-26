# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.utils import formatdate

# # Email configuration
# sender_email = 'kant.jatin@gmail.com'
# receiver_email = 'nf.ndiaye@reselform.fr'
# subject = 'Subject of the Email'
# message = 'This is the message content for testing'
# date = 'Thu, 01 Oct 2022 10:00:00 -0700'  # Set the desired past date and time

# # Create a MIMEText object
# msg = MIMEMultipart()
# msg['From'] = sender_email
# msg['To'] = receiver_email
# msg['Subject'] = subject
# msg['Date'] = date  # Set the past date and time
# msg.attach(MIMEText(message, 'plain'))

# # SMTP server configuration (for Gmail)
# smtp_server = 'smtp.gmail.com'
# smtp_port = 587
# smtp_username = 'kant.jatin55@gmail.com'
# smtp_password = 'blmcqarkyklglcwr'  # Note: Use an App Password if 2-factor authentication is enabled

# # Create an SMTP connection and send the email
# try:
#     server = smtplib.SMTP(smtp_server, smtp_port)
#     server.starttls()
#     server.login(smtp_username, smtp_password)
#     text = msg.as_string()
#     server.sendmail(sender_email, receiver_email, text)
#     server.quit()
#     print('Email sent successfully with the past date and time!')
# except Exception as e:
#     print('Email sending failed. Error: ', str(e))


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

# Function to send the email with a past date
def send_email(sender_email, receiver_email, subject, message, date):
    # Create a MIMEText object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    msg['Date'] = date  # Set the past date and time

    # SMTP server configuration (for Gmail)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'kant.jatin55@gmail.com'
    smtp_password = 'blmcqarkyklglcwr'  # Note: Use an App Password if 2-factor authentication is enabled

    # Create an SMTP connection and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print('Email sent successfully with the past date and time!')
    except Exception as e:
        print('Email sending failed. Error: ', str(e))

# Set the past date and time for the email
past_date = 'Thu, 01 Oct 2022 10:00:00 -0700'  # Set the desired past date and time

# Call the send_email function with the past date
send_email('kant.jatin55@gmail.com', 'l.dulac@reselform.fr', 'Testing', 'This is the message content', past_date)
