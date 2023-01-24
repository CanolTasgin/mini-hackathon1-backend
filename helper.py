import smtplib
import os
import json

"""
1. Go to your Google Account settings.
2. Click on "Security"
3. Under "Signing in to Google," click on "App Passwords"
4. Select "Other (Custom Name)"
5. Enter a name for the application you are using to send email (e.g. "Python Script").
6. Click on "Generate"
7. The App Password will be displayed. Use this password in the script instead of your regular password.

"""

def send_email(msg):
    subject="Test Email in from a HTS workshop"
    try:
        sender_email = os.environ.get("SENDER_EMAIL")
        sender_password = os.environ.get("SENDER_PASSWORD")
        receiver_email = os.environ.get("RECEIVER_EMAIL")
    except:
        print("""please define SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL in ENV VAR e.g
                export SENDER_EMAIL=AAA@gmail.com
                export SENDER_PASSWORD=password123
                export RECEIVER_EMAIL=BBB@gmail.com
                """ )


    message = """Subject: {subject} \n\n
    This is a test email sent using Python.
    Custom String can be added here: {msg}""".format(subject=subject,msg=msg)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email. {e}")
    finally:
        server.quit()

def history_tracker(user_data_path, email):
    target_field = 'calories'
    threshold = 150
    target_record = {}
    alert_bool = False
    with open(user_data_path, "r") as f:
        user_data = json.load(f)
        target_record = user_data[email]["food_consumed"]

    for timestamp, food_records in target_record.items():
        total_amount_per_timestamp = 0
        for food in food_records:
            if target_field in food:
                total_amount_per_timestamp+=food[target_field]

        if total_amount_per_timestamp > threshold:
            print("{} is exceeding the {} threshold({} at {})".format(email, target_field, threshold, str(timestamp)))
            alert_bool = True
    return alert_bool


            

    


    

    

