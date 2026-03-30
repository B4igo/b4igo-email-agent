#!/usr/bin/env python3
"""
Seed the test mail server with accounts and test emails.

1. Creates accounts via docker-mailserver's setup.sh (exec into mailserver).
2. Sends test emails to every account from every other account via SMTP.
"""

import json
import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

MAIL_HOST = os.environ.get("MAIL_HOST", "mailserver")
MAIL_DOMAIN = os.environ.get("MAIL_DOMAIN", "test.local")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 25))
EMAILS_PER_PAIR = int(os.environ.get("EMAILS_PER_PAIR", 3))

ACCOUNTS_FILE = Path(__file__).parent / "accounts.json"

SUBJECTS = [
    "Project update",
    "Meeting notes from today",
    "Quick question about the report",
    "Lunch plans?",
    "Action items from standup",
    "FYI: deployment schedule",
    "Re: budget review",
    "Invitation: team offsite",
    "Document review request",
    "Weekly status report",
]

BODIES = [
    "Hi,\n\nJust wanted to follow up on our earlier conversation. Let me know if you have any questions.\n\nBest regards",
    "Hey,\n\nHere are the notes from today's meeting:\n- Item 1: discussed roadmap\n- Item 2: reviewed timeline\n- Item 3: assigned action items\n\nThanks",
    "Hi there,\n\nCould you take a look at the attached document and provide feedback by end of week?\n\nAppreciate it!",
    "Hello,\n\nThis is a reminder about the upcoming deadline. Please make sure all deliverables are submitted on time.\n\nRegards",
    "Hi,\n\nI wanted to share some updates on the project:\n\n1. Phase 1 is complete\n2. Phase 2 starts next week\n3. We're on track for the deadline\n\nLet me know if you have concerns.",
]

# Automated / notification emails sent to every account.
# Each entry: (sender_name, sender_local, subject, body)
AUTOMATED_EMAILS = [
    # --- Appointment reminders ---
    (
        "Dr. Sarah Mitchell - Lakewood Family Medicine",
        "appointments@lakewoodfamilymed",
        "Appointment Reminder: Tuesday, March 24 at 10:30 AM",
        "This is a reminder that you have an upcoming appointment.\n\n"
        "Provider: Dr. Sarah Mitchell\n"
        "Date: Tuesday, March 24, 2026\n"
        "Time: 10:30 AM\n"
        "Location: Lakewood Family Medicine, 450 Oak Street, Suite 200\n\n"
        "Please arrive 15 minutes early to complete any necessary paperwork.\n"
        "If you need to cancel or reschedule, please call (555) 234-5678 at least "
        "24 hours in advance.\n\n"
        "Thank you,\nLakewood Family Medicine",
    ),
    (
        "Bright Smiles Dental",
        "no-reply@brightsmilesdental",
        "Reminder: Dental Cleaning - March 27 at 2:00 PM",
        "Hello,\n\n"
        "This is a friendly reminder about your upcoming dental cleaning.\n\n"
        "Date: Friday, March 27, 2026\n"
        "Time: 2:00 PM\n"
        "Provider: Dr. James Park, DDS\n"
        "Location: 1280 Elm Ave, Suite 4B\n\n"
        "Please remember to brush and floss before your visit. If you have any "
        "changes to your medical history or medications, let us know when you arrive.\n\n"
        "To reschedule, reply to this email or call (555) 876-5432.\n\n"
        "See you soon!\nBright Smiles Dental Team",
    ),
    (
        "ClearView Eye Care",
        "reminders@clearvieweye",
        "Your eye exam is coming up - April 2, 2026",
        "Dear Patient,\n\n"
        "You have an eye exam scheduled with Dr. Anita Rao.\n\n"
        "Date: Thursday, April 2, 2026\n"
        "Time: 11:15 AM\n"
        "Location: ClearView Eye Care, 900 Pine Blvd\n\n"
        "If you wear contact lenses, please bring your current prescription information. "
        "Bring sunglasses as your pupils may be dilated during the exam.\n\n"
        "Confirm or reschedule: (555) 321-9988\n\n"
        "ClearView Eye Care",
    ),
    (
        "PetVet Animal Hospital",
        "appointments@petvetah",
        "Vaccination appointment for your pet - March 30",
        "Hello,\n\n"
        "This is a reminder that your pet has an upcoming vaccination appointment.\n\n"
        "Date: Monday, March 30, 2026\n"
        "Time: 3:45 PM\n"
        "Veterinarian: Dr. Kevin Torres\n"
        "Location: PetVet Animal Hospital, 222 Maple Drive\n\n"
        "Please bring any previous vaccination records if this is your first visit.\n"
        "Keep your pet on a leash or in a carrier when entering the clinic.\n\n"
        "Questions? Call us at (555) 444-7890.\n\n"
        "PetVet Animal Hospital",
    ),

    # --- Shipping / delivery ---
    (
        "FedEx",
        "tracking-updates@fedex",
        "Your package is out for delivery",
        "Your package is on its way!\n\n"
        "Tracking Number: 7749 2810 3345 6621\n"
        "Estimated Delivery: Today by end of day\n"
        "Ship From: Portland, OR\n"
        "Ship To: Your address on file\n\n"
        "You can track your package in real time at fedex.com/tracking.\n\n"
        "Thank you for choosing FedEx.",
    ),
    (
        "Amazon.com",
        "shipment-tracking@amazon",
        "Your Amazon order has shipped!",
        "Hello,\n\n"
        "Great news — your order has shipped!\n\n"
        "Order #112-9374856-2938471\n"
        "Items: Wireless Bluetooth Headphones, USB-C Charging Cable (2-pack)\n"
        "Carrier: UPS\n"
        "Tracking Number: 1Z999AA10123456784\n"
        "Estimated delivery: March 19-21, 2026\n\n"
        "Track your package on Amazon.com under Your Orders.\n\n"
        "Thank you for shopping with us!",
    ),

    # --- Password reset / security ---
    (
        "GitHub",
        "noreply@github",
        "[GitHub] Password reset request",
        "We received a request to reset the password for your account.\n\n"
        "If you made this request, click the link below to set a new password:\n"
        "https://github.example.com/password_reset/abc123def456\n\n"
        "This link will expire in 24 hours.\n\n"
        "If you did not request a password reset, you can ignore this email. "
        "Your password will remain unchanged.\n\n"
        "Thanks,\nThe GitHub Team",
    ),
    (
        "Google",
        "no-reply@accounts.google",
        "Security alert: New sign-in from Windows",
        "A new sign-in was detected on your account.\n\n"
        "Device: Windows PC\n"
        "Location: Denver, CO, United States\n"
        "Time: March 16, 2026 at 3:42 PM MST\n\n"
        "If this was you, no further action is needed.\n"
        "If you don't recognize this activity, please review your account "
        "security settings immediately.\n\n"
        "— Google Accounts Team",
    ),

    # --- Newsletters / marketing ---
    (
        "Spotify",
        "no-reply@spotify",
        "Your 2026 playlist is ready!",
        "Hey there,\n\n"
        "We've put together a personalized playlist based on what you've been "
        "listening to this month.\n\n"
        "Your top genres: Indie Rock, Lo-fi, Jazz\n"
        "New discoveries: 12 tracks we think you'll love\n\n"
        "Open Spotify to start listening.\n\n"
        "Enjoy the music!\nThe Spotify Team",
    ),
    (
        "LinkedIn",
        "messages-noreply@linkedin",
        "You appeared in 14 searches this week",
        "Hi,\n\n"
        "Your profile has been getting attention:\n\n"
        "- You appeared in 14 searches this week\n"
        "- 3 people viewed your profile\n"
        "- Your post received 8 reactions\n\n"
        "See who's looking at your profile on LinkedIn.\n\n"
        "LinkedIn Notifications",
    ),

    # --- Banking / finance ---
    (
        "Chase Bank",
        "no-reply@chase",
        "Your statement is ready",
        "Dear Customer,\n\n"
        "Your monthly statement for account ending in 4821 is now available.\n\n"
        "Statement Period: February 1 - February 28, 2026\n"
        "Balance: $3,247.89\n"
        "Minimum Payment Due: $35.00\n"
        "Payment Due Date: March 25, 2026\n\n"
        "Log in to chase.com to view your full statement.\n\n"
        "Thank you,\nChase Customer Service",
    ),
    (
        "Venmo",
        "venmo@venmo",
        "You paid Alex $24.50",
        "You paid Alex R. $24.50.\n\n"
        "Note: \"Pizza last night\"\n"
        "Date: March 15, 2026\n"
        "Funded by: Venmo balance\n\n"
        "Questions? Visit the Venmo Help Center.\n\n"
        "— Venmo",
    ),

    # --- Utility / services ---
    (
        "Pacific Gas & Electric",
        "notifications@pge",
        "Your electricity bill is due March 28",
        "Dear Customer,\n\n"
        "Your electricity bill for the period February 14 - March 13, 2026 is ready.\n\n"
        "Account Number: ****6739\n"
        "Amount Due: $142.37\n"
        "Due Date: March 28, 2026\n\n"
        "You can pay online at pge.com, by phone, or by mail.\n"
        "Enrolled in AutoPay? No action needed — we'll charge your payment method on file.\n\n"
        "Thank you,\nPG&E Customer Service",
    ),
    (
        "Hermes Delivery",
        "no-reply@hermes",
        "We missed you! Redelivery options available",
        "Hi,\n\n"
        "We tried to deliver your parcel today but nobody was home.\n\n"
        "Tracking ID: HRM-88429371\n"
        "Sender: ASOS.com\n\n"
        "Your options:\n"
        "1. Redeliver tomorrow\n"
        "2. Collect from local ParcelShop (open until 8 PM)\n"
        "3. Leave in a safe place\n\n"
        "Choose your preference by replying to this email or visiting hermes.com/redelivery.\n\n"
        "Hermes Delivery Team",
    ),

    # --- Calendar / events ---
    (
        "Eventbrite",
        "info@eventbrite",
        "Your tickets for Tech Meetup - March 22",
        "You're going!\n\n"
        "Event: Downtown Tech Meetup: AI & Open Source\n"
        "Date: Sunday, March 22, 2026\n"
        "Time: 6:00 PM - 9:00 PM\n"
        "Venue: The Innovation Hub, 88 First Street\n\n"
        "Tickets: 1x General Admission\n"
        "Order #: EVB-30958271\n\n"
        "Show this email or the QR code in the Eventbrite app at the door.\n\n"
        "See you there!",
    ),
    (
        "Zoom",
        "no-reply@zoom",
        "Reminder: Team Standup starts in 15 minutes",
        "Hi,\n\n"
        "This is a reminder that your meeting is about to start.\n\n"
        "Topic: Team Standup\n"
        "Time: March 16, 2026 09:00 AM (Mountain Time)\n"
        "Duration: 30 minutes\n\n"
        "Join Zoom Meeting:\n"
        "https://zoom.example.com/j/98765432100?pwd=abcDEF123\n\n"
        "Meeting ID: 987 6543 2100\n"
        "Passcode: 112233\n\n"
        "One tap mobile: +16699006833,,98765432100#\n\n"
        "— Zoom",
    ),
]


def wait_for_smtp(host: str, port: int, retries: int = 60, delay: float = 2.0):
    """Block until SMTP is accepting connections."""
    for attempt in range(retries):
        try:
            with smtplib.SMTP(host, port, timeout=5) as srv:
                srv.noop()
                print(f"SMTP ready on {host}:{port}")
                return
        except Exception:
            print(f"Waiting for SMTP ({attempt + 1}/{retries})...")
            time.sleep(delay)
    raise RuntimeError(f"SMTP not available on {host}:{port} after {retries} attempts")


def load_accounts() -> list[dict]:
    with open(ACCOUNTS_FILE) as f:
        return json.load(f)


def provision_accounts(accounts: list[dict]):
    """Create mailserver accounts by writing postfix-accounts.cf directly.

    docker-mailserver reads /tmp/docker-mailserver/postfix-accounts.cf which is
    bind-mounted from ./config/. We write hashed entries there and then trigger
    a reload.  However, since we're in a *separate* container, we instead
    deliver mail to each address — Postfix + Dovecot with PERMIT_DOCKER=network
    will auto-create the mailbox on first delivery.

    Accounts still need to exist for IMAP login, so we create them via the
    setup script executed on the mailserver container. Since we can't exec into
    the mailserver from here, we pre-generate the accounts file.
    """
    # We write the accounts file that docker-mailserver uses. The format is:
    #   user@domain|{SHA512-CRYPT}hash
    # We use doveadm to hash, but since we don't have it here, we use a
    # simple approach: write plaintext and let setup.sh handle it.
    #
    # Actually, the simplest approach: just send mail. With PERMIT_DOCKER=network,
    # Postfix will accept mail for any address at the domain. Dovecot will create
    # the mailbox. For IMAP *login* we need real accounts though.
    #
    # The accounts are pre-written to config/postfix-accounts.cf by the
    # create_accounts_file() function below, which runs BEFORE docker compose up.
    print(f"Accounts expected to be pre-provisioned ({len(accounts)} accounts)")


def create_accounts_config(accounts: list[dict]) -> str:
    """Generate postfix-accounts.cf content.

    This is called at build time to bake the file into the config volume.
    Format: user@domain|{PLAIN}password
    (docker-mailserver hashes on first startup)
    """
    lines = []
    for acct in accounts:
        # DMS accepts {PLAIN} passwords and hashes them on startup
        lines.append(f"{acct['email']}|{{PLAIN}}{acct['password']}")
    return "\n".join(lines) + "\n"


def send_test_emails(accounts: list[dict]):
    """Send test emails between all account pairs."""
    total = 0
    subject_idx = 0
    body_idx = 0

    with smtplib.SMTP(MAIL_HOST, SMTP_PORT, timeout=30) as smtp:
        for sender in accounts:
            for recipient in accounts:
                if sender["email"] == recipient["email"]:
                    continue
                for i in range(EMAILS_PER_PAIR):
                    msg = MIMEMultipart()
                    msg["From"] = sender["email"]
                    msg["To"] = recipient["email"]
                    msg["Subject"] = f"{SUBJECTS[subject_idx % len(SUBJECTS)]} (#{i+1})"
                    msg.attach(MIMEText(BODIES[body_idx % len(BODIES)], "plain"))

                    smtp.sendmail(sender["email"], [recipient["email"]], msg.as_string())
                    total += 1
                    subject_idx += 1
                    body_idx += 1

    print(f"Sent {total} person-to-person emails across {len(accounts)} accounts")


def send_automated_emails(accounts: list[dict]):
    """Send automated/notification emails to every account."""
    total = 0

    with smtplib.SMTP(MAIL_HOST, SMTP_PORT, timeout=30) as smtp:
        for sender_name, sender_local, subject, body in AUTOMATED_EMAILS:
            sender_addr = f"{sender_local}@{MAIL_DOMAIN}"
            for recipient in accounts:
                msg = MIMEMultipart()
                msg["From"] = f"{sender_name} <{sender_addr}>"
                msg["To"] = recipient["email"]
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain"))

                smtp.sendmail(sender_addr, [recipient["email"]], msg.as_string())
                total += 1

    print(f"Sent {total} automated/notification emails to {len(accounts)} accounts")


def main():
    accounts = load_accounts()

    # Write the accounts config file so docker-mailserver picks them up.
    # This is mounted at /tmp/docker-mailserver/postfix-accounts.cf
    config_content = create_accounts_config(accounts)
    config_path = Path("/tmp/docker-mailserver/postfix-accounts.cf")
    if config_path.parent.exists():
        config_path.write_text(config_content)
        print(f"Wrote {len(accounts)} accounts to {config_path}")

    wait_for_smtp(MAIL_HOST, SMTP_PORT)

    # Give dovecot/postfix a moment to reload after accounts file change
    print("Waiting for account provisioning to settle...")
    time.sleep(5)

    send_test_emails(accounts)
    send_automated_emails(accounts)
    print("Seeding complete!")


if __name__ == "__main__":
    main()
