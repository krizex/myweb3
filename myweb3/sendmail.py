from sendgrid import Mail, SendGridAPIClient
from .config import Config
import logging

log = logging.getLogger(__name__)

email_from_address = "mike-no-reply@krizex.xyz"
email_to_address = "krizex@gmail.com"


def build_message(subject, content):
    """Builds an outgoing message."""
    message = Mail(
        from_email=email_from_address,
        to_emails=email_to_address,
        subject=subject,
        html_content='<strong>%s</strong>' % content
    )
    return message


def send_mail(subject, content):
    """Sends a built outgoing message."""
    # @todo validation & error handling.
    sg = SendGridAPIClient(Config["SENDGRID_API_KEY"])
    log.info("Send email")
    sg.send(build_message(subject, content))
