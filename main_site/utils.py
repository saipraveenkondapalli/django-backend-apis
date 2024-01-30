import smtplib

import django.utils.log
import requests
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import MainSiteContact


def get_ip_address_data(ip_add):
    url = f'http://ip-api.com/json/{ip_add}'
    data = requests.get(url).json()
    if data:
        return data

    return None


class EmailHandler:
    def __init__(self):
        self.sender = settings.DEFAULT_FROM_EMAIL
        self.job_application_receiver = settings.JOB_APPLICATION_RECEIVER
        self.contact_receiver = settings.CONTACT_RECEIVER

    def send_email(self, subject, receiver, message):
        try:
            send_mail(
                subject=subject,
                message='',
                html_message=message,
                from_email=self.sender,
                recipient_list=[receiver],
                fail_silently=False,
            )
        except smtplib.SMTPDataError as e:
            pass
        except Exception as e:
            pass
            raise Exception('Error sending email')

    def send_company_track_alert(self, company):
        subject = f"Company Track Alert - {company.company_name}"
        message = render_to_string('main_site/email/track.html', {'company': company})
        self.send_email(subject, self.job_application_receiver, message)

    def send_contact_email(self, contact: MainSiteContact):
        subject = f"Contact Email - {contact.name}"
        message = render_to_string('main_site/email/contact.html', {'contact': contact})
        self.send_email(subject, self.job_application_receiver, message)
