from django.db import models

from config import settings


class Course(models.Model):
    """Registering model Course"""

    name = models.CharField(
        max_length=300,
        verbose_name="Name",
    )

    description = models.TextField(verbose_name="Description")

    preview = models.ImageField(
        upload_to="materials/course/preview/%Y/%m/%d/",
        default=None,
        null=True,
        blank=True,
        verbose_name="Saved course preview",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="users_courses",
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = [
            "name",
        ]


class Lesson(models.Model):
    """Registering model Lesson"""

    name = models.CharField(
        max_length=300,
        verbose_name="Name",
    )

    description = models.TextField(verbose_name="Description")

    preview = models.ImageField(
        upload_to="materials/lessons/preview/%Y/%m/%d/",
        default=None,
        null=True,
        blank=True,
        verbose_name="Saved course preview",
    )

    url_link = models.URLField(max_length=200, null=True, blank=True)

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="lessons",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="users_lessons",
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        ordering = [
            "name",
        ]


class Subscription(models.Model):
    """Registering model Subscription"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="users_subscription",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="course_subscription",
    )

    subscription = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} for course {self.course}"

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
