import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import random
from database import insert_candidate

# ✅ Replace with your actual email and Gmail App Password
SENDER_EMAIL = "arjavship@gmail.com"
APP_PASSWORD = "likc ydat skwz ivnz"  # Use Gmail App Password

def generate_random_interview():
    # Random date within next 7 days
    start_date = datetime.now()
    interview_date = start_date + timedelta(days=random.randint(1, 7))

    # Random time between 10 AM – 5 PM
    hour = random.randint(10, 17)
    minute = random.choice([0, 15, 30, 45])
    formatted_time = f"{hour if hour <= 12 else hour - 12}:{minute:02d} {'AM' if hour < 12 else 'PM'}"

    # Google Meet style link
    link = f"https://meet.google.com/" \
           f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3))}-" \
           f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=4))}-" \
           f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3))}"

    return interview_date.strftime("%A, %B %d, %Y"), formatted_time, link

def send_mail(to_email, job, candidate_id="Candidate", score=0):
    try:
        date, time, link = generate_random_interview()

        # Email content
        body = f"""Dear {candidate_id},

Congratulations! 🎉

You have been shortlisted for the role of {job}.

📅 Interview Date: {date}  
⏰ Time: {time}  
🔗 Meet Link: {link}

We look forward to speaking with you.

Best regards,  
SmartHire AI Team
"""

        msg = MIMEText(body)
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = f"Interview Invitation for {job}"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()

        print(f"✅ Email sent to {to_email} for {job}!")

        # Save to SQLite database
        insert_candidate(candidate_id, to_email, job, score, date, time, link)
        print(f"💾 Saved {candidate_id} to DB")

        return True

    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
        return False
