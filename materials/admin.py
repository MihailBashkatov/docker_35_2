from django.contrib import admin

from .models import Course, Lesson, Subscription


# Register admin for Receiver model
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Registering User in Admin"""

    list_display = ("id", "name", "owner")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Registering User in Admin"""

    list_display = ("id", "name", "owner")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Registering User in Subscription"""

    list_display = ("id", "user", "course", "subscription")
