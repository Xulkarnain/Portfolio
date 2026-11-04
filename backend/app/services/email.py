import json
import logging
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from app.core.config import settings

logger = logging.getLogger(__name__)


def send_contact_notification(
    visitor_name: str,
    visitor_email: str,
    subject: str,
    message: str,
) -> bool:
    """Send a contact form notification using Resend."""

    payload = {
        "from": "Portfolio Contact <onboarding@resend.dev>",
        "to": [settings.contact_notification_email],
        "reply_to": visitor_email,
        "subject": f"Portfolio Contact: {subject}",
        "text": (
            f"Name: {visitor_name}\n"
            f"Email: {visitor_email}\n"
            f"Subject: {subject}\n\n"
            f"Message:\n{message}"
        ),
    }

    request = Request(
        url="https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {settings.resend_api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=10) as response:
            if response.status in (200, 201):
                logger.info("Contact notification email sent successfully.")
                return True

            logger.warning(
                "Resend returned unexpected status: %s",
                response.status,
            )
            return False

    except HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")

        logger.error(
            "Resend API request failed. Status: %s, Response: %s",
            error.code,
            error_body,
        )
        return False

    except (URLError, TimeoutError, OSError):
        logger.exception("Unable to send contact notification email.")
        return False