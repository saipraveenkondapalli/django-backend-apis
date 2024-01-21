import requests
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import MainSiteContact


def get_ip_address_data(ip_add):
    ip_add = '223.196.171.245'
    url = f'http://ip-api.com/json/{ip_add}'
    data = requests.get(url).json()
    if data:
        return data

    return None


class EmailHandler:
    def __init__(self):
        self.sender = settings.EMAIL_HOST_USER
        self.job_application_receiver = settings.JOB_APPLICATION_RECEIVER
        self.contact_receiver = settings.CONTACT_RECEIVER

    def send_email(self, subject, to, message):
        send_mail(
            subject=subject,
            message='',
            recipient_list=[to],
            from_email=self.sender,
            html_message=message,
            fail_silently=False,
        )

    def send_company_track_alert(self, company):
        subject = f"Company Track Alert - {company.company_name}"
        message = render_to_string('main_site/email/track.html', {'company': company})
        self.send_email(subject, self.job_application_receiver, message)

    def send_contact_email(self, contact: MainSiteContact):
        subject = f"Contact Email - {contact.name}"
        message = render_to_string('main_site/email/contact.html', {'contact': contact})
        self.send_email(subject, self.job_application_receiver, message)



