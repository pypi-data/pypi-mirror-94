import logging

from typing import List
from sendgrid import SendGridAPIClient, HtmlContent, Mail, Attachment, DynamicTemplateData

logger = logging.getLogger('remo_app')


def send_user_feedback(user_email: str, payload: dict, attachment: Attachment = None):
    from django.conf import settings
    mail = compose_template_mail(
        emails=settings.EMAIL_LIST,
        template_id='d-2bc420d20a6d44a2856d1fc07f9c24f9',
        template_data=payload,
        from_email=user_email
    )
    mail.subject = f'Remo feedback from {payload.get("fullname")}'
    if attachment:
        mail.attachment = attachment

    return send(mail)


def send_email(
        subject: str, content: str,
        from_email: str = None, to_emails: List[str] = None,
        attachment: Attachment = None
) -> bool:
    from django.conf import settings
    if not from_email:
        from_email = settings.REMO_EMAIL
    if not to_emails:
        to_emails = settings.EMAIL_LIST

    mail = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=HtmlContent(content),
    )

    if attachment:
        mail.attachment = attachment

    return send(mail)


def send_user_credentials(email: str, password: str, admin_email: str, user_name: str):
    from django.conf import settings
    send(
        compose_template_mail(
            [email], "d-6743c4be561b44da981678db972ee929",
            {
                "user_name": user_name,
                "password": password,
                "domain": f"http://{settings.DOMAIN}",
                "admin_email": admin_email,
            }
        )
    )


def send(msg: Mail) -> bool:
    from django.conf import settings
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(msg)
        return True
    except Exception as err:
        logger.error(f'Failed to send email: {err}')
    return False


def compose_template_mail(emails: List[str], template_id: str, template_data: dict, from_email: str = None) -> Mail:
    from django.conf import settings
    if not from_email:
        from_email = settings.REMO_EMAIL

    mail = Mail(from_email=from_email, to_emails=emails,)
    mail.template_id = template_id
    mail.dynamic_template_data = DynamicTemplateData(
        dynamic_template_data=template_data
    )
    return mail


def compose_msg(req, resp):
    return f"""
<html>
    <body>
        <p>Failed to register user: </br>
        Request: {req}. </br>
        Response: {resp}</p>
    </body>
</html>
"""

