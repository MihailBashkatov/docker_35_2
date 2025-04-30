import datetime

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from users.models import User


@shared_task
def send_update_course_info(users_list, course_name):
    """Task to send email about Course changing for subscribed users"""
    send_mail(
        subject=f"Updated info for course {course_name}",
        message=f"The course {course_name} has been updated. Please, check details",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=users_list,
    )


@shared_task
def last_login():
    """Task to identify last user login. If login happens more than 1 month ago, user becomes Inactive"""

    today = timezone.now().today()  # gets current date
    user_is_active = User.objects.filter(is_active=True)  # gets active users
    valid_interval = today - datetime.timedelta(
        days=30
    )  # sets interval 30 days in the past from today

    for user in user_is_active:
        user_last_login = user.last_login.date()  # gets last login date

        if user_last_login < valid_interval.date():

            user.is_active = False  # sets user in_active on 31st day after last login
            user.save()
