from django.shortcuts import get_object_or_404

from materials.models import Course


def get_course(pk):
    """Return particular course"""
    return get_object_or_404(Course, pk=pk)


def get_users_subscribed(pk):
    """Return list of the subscribed users for particular course"""
    course = get_course(pk)
    users_subscribed = course.course_subscription.filter(subscription=True)
    users_list = []
    if users_subscribed:
        for user in users_subscribed:
            users_list.append(user.user.email)
    return users_list
