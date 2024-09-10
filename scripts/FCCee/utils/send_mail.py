import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

# Create a text/plain message
msg = EmailMessage()
with open('mail_body.txt', 'r') as file:
    content = file.read()
msg.set_content(content)

msg['Subject'] = f'Test email'
msg['From'] = 'FCC.FullSim.validation@cern.ch'
msg['To'] = 'enrico.lupi@cern.ch'

# Send the message via our own SMTP server.
s = smtplib.SMTP('cernmx.cern.ch')
s.send_message(msg)
s.quit()