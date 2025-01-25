from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


def detect_user(user):
    if user.role == 1:
        redirectUrl = "/accounts/vendor-dashboard/"
        return redirectUrl
    elif user.role == 2:
        redirectUrl = "/accounts/customer-dashboard/"
        return redirectUrl
    elif user.role == None:
        redirectUrl = "/admin"
        return redirectUrl
    
def send_verification_email(request, user):
    current_site = get_current_site(request)
    mail_subject = "Please activate your account"
    message = render_to_string('accounts/email/email_verification.html', {
        'user': user, 
        'domain': current_site.domain,  # Corrected: use .domain
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)
    })
    
    to_email = user.email
    mail = EmailMessage(
        mail_subject, 
        message, 
        from_email=settings.EMAIL_HOST_USER, 
        to=[to_email]
    )
    mail.content_subtype = 'html'  
    mail.send()

def send_password_reset_email(request, user):
    current_site = get_current_site(request)
    mail_subject = "Reset Password Link"
    message = render_to_string('accounts/email/email_forgot_password.html',{
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)
    })

    to_email = user.email
    mail = EmailMessage(
        mail_subject,
        message,
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email]
    )
    mail.content_subtype = 'html'
    mail.send()