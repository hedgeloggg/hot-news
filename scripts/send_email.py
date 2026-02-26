# scripts/send_email.py
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def main():
    with open('output/final_report.txt') as f:
        content = f.read()
    
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = Header("热点雷达", 'utf-8')
    msg['To'] = Header("你", 'utf-8')
    msg['Subject'] = Header("【全球社交热点日报】", 'utf-8')
    
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
        server.sendmail(
            os.getenv('EMAIL_USER'),
            os.getenv('TO_EMAIL'),
            msg.as_string()
        )
        server.quit()
        print("✅ Email sent successfully")
    except Exception as e:
        print(f"📧 Email Error: {e}")

if __name__ == '__main__':
    main()
