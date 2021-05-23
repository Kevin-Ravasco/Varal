from smtplib import SMTPException
from socket import gaierror

from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_job_allocation_email(user, job,  to_email, site):
    message = render_to_string('job_email.html', {'user': user, 'job': job, 'domain': site.domain})
    mail_subject = 'Applied Job Details'
    try:
        send_mail(mail_subject, message, '<youremail>', [to_email])
        return 'success'
    except (ConnectionAbortedError, SMTPException, gaierror):
        return "error"