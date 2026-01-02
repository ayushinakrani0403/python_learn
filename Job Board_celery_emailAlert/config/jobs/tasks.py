# jobs/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Job

@shared_task
def send_job_alert_email(job_id):
    job = Job.objects.get(id=job_id)

    send_mail(
        subject=f'New Job Posted: {job.title}',
        message=(
            f"Company: {job.company}\n"
            f"Location: {job.location}\n\n"
            f"{job.description}"
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['ayushinakrani97@gmail.com'],  # change receiver email
        fail_silently=False,
    )
