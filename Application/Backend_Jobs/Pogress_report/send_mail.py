import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


from Application.config import SMTPConfig




def send_mail(filename,name,email,message_html=None):
  try:  
    msg = MIMEMultipart()
    msg['From'] = SMTPConfig.SENDER_ADDRESS
    msg['To'] = email
    msg['Subject'] = name+" Monthly Progress Report"
    body = "Hi "+name+",\n\nPlease find the attached progress report for the month.\n\nRegards,\nRavineel"
    msg.attach(MIMEText(body, 'plain'))
    if message_html:
      msg.attach(MIMEText(message_html, 'html'))
    else:
      msg.attach(MIMEApplication(open(filename, "rb").read()))

    s = smtplib.SMTP(host=SMTPConfig.SMPTP_SERVER_HOST, port=SMTPConfig.SMPTP_SERVER_PORT)
    s.login(SMTPConfig.SENDER_ADDRESS, SMTPConfig.SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return 1
  except:
    print("eror")
