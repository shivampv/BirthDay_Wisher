import smtplib
import datetime as dt
import os
import csv
import time
from dotenv import load_dotenv
import schedule

print("\n--- Birthday Wisher ---")

# Load env file check the .env file for instruction
load_dotenv()
my_email = os.getenv("EMAIL_ID")
my_password = os.getenv("APP_PASSWORD")

# On which time its should check 00:00 means 12AM  (24hr)format. 
timestamp = '00:00'

# Add friends details
def add_friend():
    name = input("Enter your friend's name: ")
    email = input(f"Enter {name}'s email: ")
    dob = input(f"Enter {name}'s date of birth (YYYY-MM-DD): ")
    
    # Save details to CSV
    with open("friends.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, email, dob])
    print(f"{name}'s details have been saved successfully!")

# Check for birthdays and send emails
def check_and_send_birthday_emails():
    today = dt.datetime.now().strftime("%m-%d")
    try:
        with open("friends.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                name, email, dob = row
                dob_month_day = "-".join(dob.split("-")[1:])
                if today == dob_month_day:
                    # Send email
                    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                        connection.starttls()
                        connection.login(user=my_email, password=my_password)
                        message = f"Subject: Happy Birthday, 🤍🤍{name}🤍🤍!\n\nDear {name},\n\nWishing you a fantastic birthday filled with love and happiness!"
                        connection.sendmail(
                            from_addr=my_email,
                            to_addrs=email,
                            msg=message.encode("utf-8")
                        )
                    print(f"Birthday email sent to {name} ({email})!")
    except FileNotFoundError:
        print("No friends saved yet. Add some friends first!")

# scheduler
def continuous_check():
    schedule.every().day.at(timestamp).do(check_and_send_birthday_emails)

    print(f"The program is running and will check for birthdays daily at {timestamp} (24hr format).")
    print("Press Ctrl+C to exit.")
    while True:
        schedule.run_pending()
        time.sleep(1)

# Main menu
def main_menu():
    while True:
        print("1. Add a Friend")
        print("2. Start Continuous Birthday Check")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_friend()
        elif choice == "2":
            continuous_check()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("\n Please Choose between 1,2 or 3.")

# Run main program
if __name__ == "__main__":
    main_menu()
